"""
Module de classification automatique des titres Google Discover
Utilise une approche hybride : mots-clés + similarité sémantique
"""

import pandas as pd
import numpy as np
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import logging
from tqdm import tqdm
import joblib
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DiscoverClassifier:
    """Classificateur de titres Google Discover en 12 catégories"""
    
    def __init__(self, config_path: str = "config/categories.yaml"):
        self.config_path = Path(config_path)
        self.categories = self._load_categories()
        self.model = None
        self.category_embeddings = {}
        self._initialize_model()
        
    def _load_categories(self) -> Dict:
        """Charge la configuration des catégories"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config['categories']
    
    def _initialize_model(self):
        """Initialise le modèle de sentence embeddings français"""
        logger.info("Chargement du modèle de sentence embeddings...")
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self._compute_category_embeddings()
        
    def _compute_category_embeddings(self):
        """Calcule les embeddings pour chaque catégorie"""
        logger.info("Calcul des embeddings de catégories...")
        for cat_key, cat_data in self.categories.items():
            # Créer un texte représentatif de la catégorie
            keywords = cat_data['keywords']
            category_text = f"{cat_data['name']} {' '.join(keywords[:20])}"
            
            # Calculer l'embedding
            embedding = self.model.encode(category_text)
            self.category_embeddings[cat_key] = embedding
            
    def _keyword_score(self, title: str, keywords: List[str]) -> float:
        """Calcule le score basé sur les mots-clés"""
        title_lower = title.lower()
        matches = sum(1 for keyword in keywords if keyword in title_lower)
        return matches / len(keywords) if keywords else 0
    
    def _semantic_similarity(self, title: str, category_key: str) -> float:
        """Calcule la similarité sémantique avec une catégorie"""
        title_embedding = self.model.encode(title)
        cat_embedding = self.category_embeddings[category_key]
        
        # Reshape pour cosine_similarity
        title_emb = title_embedding.reshape(1, -1)
        cat_emb = cat_embedding.reshape(1, -1)
        
        similarity = cosine_similarity(title_emb, cat_emb)[0][0]
        return similarity
    
    def classify_title(self, title: str, threshold: float = 0.3) -> Dict:
        """
        Classifie un titre dans une ou plusieurs catégories
        
        Returns:
            Dict avec catégorie principale, secondaires et scores
        """
        scores = {}
        
        for cat_key, cat_data in self.categories.items():
            # Score hybride : mots-clés + sémantique
            keyword_score = self._keyword_score(title, cat_data['keywords'])
            semantic_score = self._semantic_similarity(title, cat_key)
            
            # Pondération : 40% mots-clés, 60% sémantique
            final_score = (0.4 * keyword_score + 0.6 * semantic_score)
            scores[cat_key] = final_score
            
        # Trier par score décroissant
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Catégorie principale
        main_category = sorted_scores[0][0]
        main_score = sorted_scores[0][1]
        
        # Catégories secondaires (score > threshold)
        secondary_categories = [
            (cat, score) for cat, score in sorted_scores[1:] 
            if score > threshold
        ][:2]  # Max 2 catégories secondaires
        
        return {
            'title': title,
            'main_category': main_category,
            'main_category_name': self.categories[main_category]['name'],
            'main_score': main_score,
            'confidence': self._calculate_confidence(sorted_scores),
            'secondary_categories': secondary_categories,
            'all_scores': dict(sorted_scores)
        }
    
    def _calculate_confidence(self, sorted_scores: List[Tuple]) -> float:
        """Calcule le score de confiance de la classification"""
        if len(sorted_scores) < 2:
            return 1.0
            
        # Différence entre les deux meilleurs scores
        diff = sorted_scores[0][1] - sorted_scores[1][1]
        
        # Normaliser entre 0 et 1
        confidence = min(diff * 2, 1.0)
        return confidence
    
    def classify_batch(self, titles: List[str], n_jobs: int = -1) -> pd.DataFrame:
        """
        Classifie un batch de titres en parallèle
        
        Args:
            titles: Liste des titres à classifier
            n_jobs: Nombre de processus (-1 pour utiliser tous les CPU)
            
        Returns:
            DataFrame avec les résultats de classification
        """
        if n_jobs == -1:
            n_jobs = mp.cpu_count()
            
        logger.info(f"Classification de {len(titles)} titres avec {n_jobs} processus...")
        
        results = []
        
        # Traitement séquentiel pour éviter les problèmes avec le modèle
        for title in tqdm(titles, desc="Classification"):
            result = self.classify_title(title)
            results.append(result)
            
        # Convertir en DataFrame
        df_results = pd.DataFrame(results)
        
        # Ajouter des colonnes supplémentaires
        df_results['category_id'] = df_results['main_category'].map(
            lambda x: self.categories[x]['id']
        )
        df_results['category_emoji'] = df_results['main_category'].map(
            lambda x: self.categories[x]['emoji']
        )
        
        return df_results
    
    def analyze_distribution(self, df_classified: pd.DataFrame) -> Dict:
        """Analyse la distribution des catégories"""
        distribution = df_classified['main_category_name'].value_counts()
        
        analysis = {
            'total_titles': len(df_classified),
            'distribution': distribution.to_dict(),
            'distribution_pct': (distribution / len(df_classified) * 100).round(2).to_dict(),
            'high_confidence_titles': len(df_classified[df_classified['confidence'] > 0.7]),
            'low_confidence_titles': len(df_classified[df_classified['confidence'] < 0.3]),
            'multi_category_titles': len(df_classified[df_classified['secondary_categories'].apply(len) > 0])
        }
        
        return analysis
    
    def save_model(self, path: str):
        """Sauvegarde le modèle et les embeddings"""
        model_data = {
            'category_embeddings': self.category_embeddings,
            'categories': self.categories
        }
        joblib.dump(model_data, path)
        logger.info(f"Modèle sauvegardé dans {path}")
        
    def load_model(self, path: str):
        """Charge le modèle et les embeddings"""
        model_data = joblib.load(path)
        self.category_embeddings = model_data['category_embeddings']
        self.categories = model_data['categories']
        logger.info(f"Modèle chargé depuis {path}")


def process_csv(input_path: str, output_path: str, title_column: str = 'Title'):
    """
    Traite un fichier CSV complet
    
    Args:
        input_path: Chemin du CSV d'entrée
        output_path: Chemin du CSV de sortie
        title_column: Nom de la colonne contenant les titres
    """
    # Charger les données
    logger.info(f"Chargement du fichier {input_path}...")
    df = pd.read_csv(input_path)
    
    if title_column not in df.columns:
        raise ValueError(f"Colonne '{title_column}' non trouvée dans le CSV")
        
    # Initialiser le classificateur
    classifier = DiscoverClassifier()
    
    # Classifier les titres
    titles = df[title_column].tolist()
    df_classified = classifier.classify_batch(titles)
    
    # Fusionner avec les données originales
    df_final = pd.concat([df, df_classified], axis=1)
    
    # Sauvegarder
    df_final.to_csv(output_path, index=False)
    logger.info(f"Résultats sauvegardés dans {output_path}")
    
    # Afficher l'analyse
    analysis = classifier.analyze_distribution(df_classified)
    logger.info(f"\n=== ANALYSE DE DISTRIBUTION ===")
    logger.info(f"Total de titres: {analysis['total_titles']}")
    logger.info(f"Titres haute confiance (>70%): {analysis['high_confidence_titles']}")
    logger.info(f"Titres basse confiance (<30%): {analysis['low_confidence_titles']}")
    logger.info(f"Titres multi-catégories: {analysis['multi_category_titles']}")
    logger.info(f"\n=== DISTRIBUTION PAR CATÉGORIE ===")
    for cat, pct in analysis['distribution_pct'].items():
        logger.info(f"{cat}: {pct}%")
        

if __name__ == "__main__":
    # Test avec quelques exemples
    test_titles = [
        "5 remèdes naturels contre le mal de dos qui fonctionnent vraiment",
        "Comment j'ai perdu 10kg en 3 mois avec cette méthode simple",
        "Les secrets anti-âge des stars françaises révélés",
        "Cette tendance société va tout changer en 2024",
        "Découvrez les plus belles régions de France pour vos vacances",
        "Ma routine bien-être du matin qui a changé ma vie",
        "L'exposition Picasso qui fait sensation à Paris",
        "Gérer son stress : les conseils d'un psychologue",
        "Retraite : ce qui change pour les seniors en 2024",
        "Les voitures électriques les plus fiables du marché",
        "Investir dans l'immobilier : le guide complet",
        "Recette facile : le gratin dauphinois parfait en 30 minutes"
    ]
    
    classifier = DiscoverClassifier()
    
    for title in test_titles:
        result = classifier.classify_title(title)
        print(f"\nTitre: {title}")
        print(f"Catégorie: {result['category_emoji']} {result['main_category_name']} (confiance: {result['confidence']:.2f})")
        if result['secondary_categories']:
            print(f"Catégories secondaires: {result['secondary_categories']}")