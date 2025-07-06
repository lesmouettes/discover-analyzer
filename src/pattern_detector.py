"""
Module de détection automatique des patterns dans les titres
Approche multi-niveaux pour extraire tous les patterns haute performance
"""

import re
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set
import logging
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

logger = logging.getLogger(__name__)

class PatternDetector:
    """Détecteur exhaustif de patterns dans les titres Google Discover"""
    
    def __init__(self):
        self.patterns = defaultdict(list)
        self._initialize_nltk()
        self._initialize_patterns()
        
    def _initialize_nltk(self):
        """Télécharge les ressources NLTK nécessaires"""
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass
            
    def _initialize_patterns(self):
        """Initialise les regex pour détecter différents types de patterns"""
        
        # Patterns d'ouverture
        self.opening_patterns = {
            'voici': r'^voici\s+',
            'decouvrez': r'^découvrez\s+',
            'comment': r'^comment\s+',
            'pourquoi': r'^pourquoi\s+',
            'cette': r'^cette?\s+',
            'ces': r'^ces\s+',
            'savez_vous': r'^savez[-\s]?vous\s+',
            'connaissez_vous': r'^connaissez[-\s]?vous\s+',
            'attention': r'^attention\s+',
            'alerte': r'^alerte\s+',
            'enfin': r'^enfin\s+',
            'nouvelle': r'^nouvelle?\s+',
            'exclusive': r'^exclusi(f|ve)\s+',
        }
        
        # Patterns de fermeture
        self.closing_patterns = {
            'minutes': r'\s+en\s+\d+\s+minutes?$',
            'jours': r'\s+en\s+\d+\s+jours?$',
            'sans_effort': r'\s+sans\s+effort$',
            'qui_marche': r'\s+qui\s+march(e|ent)$',
            'revolutionnaire': r'\s+révolutionnaire$',
            'simple': r'\s+simple$',
            'facile': r'\s+facile$',
            'gratuit': r'\s+gratuit(e)?$',
            'immediat': r'\s+imm[eé]diat(ement)?$',
        }
        
        # Patterns numériques
        self.numeric_patterns = {
            'top_x': r'\b(top\s+)?\d+\s+(meilleur|conseil|astuce|erreur|raison|façon)',
            'x_euros': r'\b\d+\s*€|euros?\b',
            'pourcentage': r'\b\d+\s*%',
            'age': r'\b(après|dès|avant|à)\s+\d+\s+ans\b',
            'annee': r'\b20\d{2}\b',
        }
        
        # Patterns d'autorité
        self.authority_patterns = {
            'expert': r'\b(expert|spécialiste|professionnel|docteur|médecin|coach)\b',
            'scientifique': r'\b(étude|recherche|science|chercheur|prouvé|démontré)\b',
            'celebrite': r'\b(star|célébrité|people|influenceur)\b',
            'temoignage': r'\b(j\'ai|mon|ma|mes|témoignage|expérience|vécu)\b',
        }
        
        # Patterns émotionnels
        self.emotional_patterns = {
            'urgence': r'\b(urgent|vite|maintenant|immédiatement|avant\s+qu)',
            'peur': r'\b(danger|attention|alerte|risque|éviter|jamais|arrêt)',
            'curiosite': r'\b(secret|révél|découv|cach|mystèr|vérité)',
            'espoir': r'\b(enfin|solution|révolution|miracle|incroyable|extraordinaire)',
            'facilite': r'\b(simple|facile|rapide|sans\s+effort|automatique)',
        }
        
    def extract_ngrams(self, titles: List[str], n_range: Tuple[int, int] = (2, 5)) -> Dict[str, int]:
        """Extrait les n-grams les plus fréquents"""
        all_ngrams = []
        
        for title in titles:
            tokens = word_tokenize(title.lower())
            for n in range(n_range[0], n_range[1] + 1):
                all_ngrams.extend([' '.join(gram) for gram in ngrams(tokens, n)])
                
        # Compter et filtrer
        ngram_counts = Counter(all_ngrams)
        # Garder seulement les n-grams apparaissant au moins 3 fois
        frequent_ngrams = {k: v for k, v in ngram_counts.items() if v >= 3}
        
        return dict(sorted(frequent_ngrams.items(), key=lambda x: x[1], reverse=True)[:100])
    
    def detect_structures(self, titles: List[str]) -> Dict[str, List[str]]:
        """Détecte les structures récurrentes dans les titres"""
        structures = defaultdict(list)
        
        for title in titles:
            title_lower = title.lower()
            
            # Détecter patterns d'ouverture
            for pattern_name, regex in self.opening_patterns.items():
                if re.search(regex, title_lower):
                    structures[f'opening_{pattern_name}'].append(title)
                    
            # Détecter patterns de fermeture
            for pattern_name, regex in self.closing_patterns.items():
                if re.search(regex, title_lower):
                    structures[f'closing_{pattern_name}'].append(title)
                    
            # Détecter patterns numériques
            for pattern_name, regex in self.numeric_patterns.items():
                if re.search(regex, title_lower):
                    structures[f'numeric_{pattern_name}'].append(title)
                    
            # Détecter patterns d'autorité
            for pattern_name, regex in self.authority_patterns.items():
                if re.search(regex, title_lower):
                    structures[f'authority_{pattern_name}'].append(title)
                    
            # Détecter patterns émotionnels
            for pattern_name, regex in self.emotional_patterns.items():
                if re.search(regex, title_lower):
                    structures[f'emotional_{pattern_name}'].append(title)
                    
        return dict(structures)
    
    def analyze_patterns_by_category(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """Analyse les patterns spécifiques à chaque catégorie"""
        category_patterns = {}
        
        for category in df['main_category_name'].unique():
            cat_titles = df[df['main_category_name'] == category]['title'].tolist()
            
            if len(cat_titles) < 5:  # Skip si pas assez de titres
                continue
                
            # Extraire patterns pour cette catégorie
            cat_structures = self.detect_structures(cat_titles)
            cat_ngrams = self.extract_ngrams(cat_titles)
            
            # Analyser les caractéristiques
            lengths = [len(title) for title in cat_titles]
            
            category_patterns[category] = {
                'total_titles': len(cat_titles),
                'structures': {k: len(v) for k, v in cat_structures.items()},
                'top_ngrams': dict(list(cat_ngrams.items())[:20]),
                'avg_length': np.mean(lengths),
                'length_range': (min(lengths), max(lengths)),
                'top_patterns': self._get_top_patterns(cat_structures, 5),
                'unique_words': self._get_unique_words(cat_titles),
            }
            
        return category_patterns
    
    def _get_top_patterns(self, structures: Dict[str, List[str]], n: int = 5) -> List[Dict]:
        """Extrait les top N patterns avec exemples"""
        top_patterns = []
        
        # Trier par fréquence
        sorted_patterns = sorted(structures.items(), key=lambda x: len(x[1]), reverse=True)[:n]
        
        for pattern_type, examples in sorted_patterns:
            top_patterns.append({
                'type': pattern_type,
                'count': len(examples),
                'examples': examples[:3]  # 3 exemples max
            })
            
        return top_patterns
    
    def _get_unique_words(self, titles: List[str]) -> List[str]:
        """Extrait les mots uniques les plus fréquents"""
        # Mots vides français à exclure
        stopwords = {'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'pour', 
                    'et', 'ou', 'à', 'avec', 'sans', 'sur', 'dans', 'par', 'en',
                    'ce', 'ces', 'cet', 'cette', 'qui', 'que', 'dont', 'où'}
        
        words = []
        for title in titles:
            tokens = word_tokenize(title.lower())
            words.extend([w for w in tokens if len(w) > 3 and w not in stopwords])
            
        word_counts = Counter(words)
        return [word for word, _ in word_counts.most_common(20)]
    
    def generate_pattern_insights(self, category_patterns: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Génère des insights actionnables par catégorie"""
        insights = {}
        
        for category, data in category_patterns.items():
            cat_insights = []
            
            # Insight sur la longueur
            avg_len = data['avg_length']
            cat_insights.append(f"Longueur optimale : {int(avg_len-10)} à {int(avg_len+10)} caractères")
            
            # Insights sur les patterns dominants
            if data['top_patterns']:
                dominant = data['top_patterns'][0]['type']
                cat_insights.append(f"Pattern dominant : {dominant.replace('_', ' ')}")
                
            # Insights sur les mots-clés
            if data['unique_words']:
                top_words = ', '.join(data['unique_words'][:5])
                cat_insights.append(f"Mots-clés performants : {top_words}")
                
            # Insights sur les structures
            structures = data['structures']
            if any('numeric' in s for s in structures):
                cat_insights.append("Les chiffres augmentent l'engagement")
                
            if any('emotional' in s for s in structures):
                cat_insights.append("Les déclencheurs émotionnels sont efficaces")
                
            insights[category] = cat_insights
            
        return insights
    
    def export_patterns(self, patterns: Dict, output_path: str):
        """Exporte les patterns détectés dans un fichier JSON"""
        import json
        
        # Convertir pour JSON (gérer les types non sérialisables)
        def convert_for_json(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
            
        patterns_json = json.dumps(patterns, default=convert_for_json, ensure_ascii=False, indent=2)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(patterns_json)
            
        logger.info(f"Patterns exportés dans {output_path}")