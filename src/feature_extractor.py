"""
Module d'extraction de features linguistiques pour l'analyse des titres
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import textstat
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """Extracteur de features linguistiques avancées"""
    
    def __init__(self):
        self.punctuation_patterns = {
            'question': r'\?',
            'exclamation': r'!',
            'ellipsis': r'\.{3}',
            'colon': r':',
            'quotes': r'[«»""]',
            'parentheses': r'[()]',
        }
        
        self.word_types = {
            'power_words': [
                'secret', 'révélé', 'incroyable', 'extraordinaire', 'miracle',
                'révolutionnaire', 'exclusif', 'urgent', 'alerte', 'danger',
                'gratuit', 'facile', 'simple', 'rapide', 'immédiat',
                'nouveau', 'découverte', 'astuce', 'méthode', 'technique'
            ],
            'emotional_words': [
                'adorer', 'aimer', 'détester', 'haïr', 'peur', 'joie',
                'bonheur', 'tristesse', 'colère', 'surprise', 'choc',
                'incroyable', 'extraordinaire', 'fantastique', 'horrible'
            ],
            'action_words': [
                'découvrir', 'apprendre', 'maîtriser', 'réussir', 'obtenir',
                'gagner', 'perdre', 'économiser', 'investir', 'acheter',
                'vendre', 'créer', 'fabriquer', 'construire', 'détruire'
            ],
            'urgency_words': [
                'maintenant', 'immédiatement', 'urgent', 'vite', 'rapidement',
                'aujourd\'hui', 'dernière', 'chance', 'limité', 'exclusif'
            ]
        }
        
    def extract_features(self, title: str) -> Dict:
        """Extrait toutes les features d'un titre"""
        features = {}
        
        # Features de base
        features['length'] = len(title)
        features['word_count'] = len(title.split())
        features['avg_word_length'] = np.mean([len(w) for w in title.split()])
        
        # Features de ponctuation
        for punct_type, pattern in self.punctuation_patterns.items():
            features[f'has_{punct_type}'] = bool(re.search(pattern, title))
            
        # Features de capitalisation
        features['has_caps'] = any(c.isupper() for c in title[1:])  # Skip première lettre
        features['all_caps_words'] = len([w for w in title.split() if w.isupper() and len(w) > 1])
        
        # Features numériques
        numbers = re.findall(r'\d+', title)
        features['has_numbers'] = len(numbers) > 0
        features['number_count'] = len(numbers)
        if numbers:
            features['first_number'] = int(numbers[0])
        else:
            features['first_number'] = 0
            
        # Features de mots spéciaux
        title_lower = title.lower()
        for word_type, words in self.word_types.items():
            count = sum(1 for word in words if word in title_lower)
            features[f'{word_type}_count'] = count
            features[f'has_{word_type}'] = count > 0
            
        # Features de lisibilité
        features['flesch_reading_ease'] = textstat.flesch_reading_ease(title)
        
        # Features de structure
        features['starts_with_number'] = bool(re.match(r'^\d+', title))
        features['starts_with_question'] = title.lower().startswith(('comment', 'pourquoi', 'quand', 'où', 'qui', 'que'))
        features['starts_with_verb'] = self._starts_with_verb(title)
        
        # Features émotionnelles
        features['emotion_score'] = self._calculate_emotion_score(title)
        features['urgency_score'] = self._calculate_urgency_score(title)
        
        return features
    
    def _starts_with_verb(self, title: str) -> bool:
        """Détecte si le titre commence par un verbe d'action"""
        action_verbs = [
            'découvrez', 'apprenez', 'essayez', 'testez', 'profitez',
            'économisez', 'gagnez', 'créez', 'évitez', 'arrêtez',
            'commencez', 'terminez', 'réussissez', 'obtenez', 'devenez'
        ]
        first_word = title.split()[0].lower()
        return any(first_word.startswith(verb[:5]) for verb in action_verbs)
    
    def _calculate_emotion_score(self, title: str) -> float:
        """Calcule un score émotionnel basé sur les mots utilisés"""
        title_lower = title.lower()
        emotion_count = sum(1 for word in self.word_types['emotional_words'] if word in title_lower)
        return emotion_count / len(title.split())
    
    def _calculate_urgency_score(self, title: str) -> float:
        """Calcule un score d'urgence"""
        title_lower = title.lower()
        urgency_count = sum(1 for word in self.word_types['urgency_words'] if word in title_lower)
        
        # Bonus pour certains patterns
        if re.search(r'avant\s+qu', title_lower):
            urgency_count += 2
        if re.search(r'dernière\s+chance', title_lower):
            urgency_count += 3
            
        return urgency_count / len(title.split())
    
    def extract_batch_features(self, titles: List[str]) -> pd.DataFrame:
        """Extrait les features pour un batch de titres"""
        features_list = []
        
        for title in titles:
            features = self.extract_features(title)
            features['title'] = title
            features_list.append(features)
            
        return pd.DataFrame(features_list)
    
    def analyze_feature_importance(self, df_features: pd.DataFrame, target_col: str = None) -> Dict:
        """Analyse l'importance des features"""
        # Features numériques seulement
        numeric_features = df_features.select_dtypes(include=[np.number]).columns.tolist()
        
        if target_col and target_col in numeric_features:
            numeric_features.remove(target_col)
            
        # Statistiques descriptives
        stats = {}
        for feature in numeric_features:
            stats[feature] = {
                'mean': df_features[feature].mean(),
                'std': df_features[feature].std(),
                'min': df_features[feature].min(),
                'max': df_features[feature].max(),
                'correlation_with_length': df_features[feature].corr(df_features['length'])
            }
            
        return stats
    
    def get_feature_recommendations(self, features: Dict) -> List[str]:
        """Génère des recommandations basées sur les features"""
        recommendations = []
        
        # Longueur
        if features['length'] < 50:
            recommendations.append("Titre trop court - visez 60-80 caractères")
        elif features['length'] > 100:
            recommendations.append("Titre trop long - réduisez à 80 caractères max")
            
        # Nombres
        if not features['has_numbers']:
            recommendations.append("Ajoutez des chiffres pour plus d'impact")
            
        # Mots puissants
        if features['power_words_count'] == 0:
            recommendations.append("Utilisez des mots puissants (secret, révélé, incroyable...)")
            
        # Questions
        if not features['has_question'] and not features['starts_with_question']:
            recommendations.append("Considérez une formulation en question")
            
        # Urgence
        if features['urgency_score'] < 0.1:
            recommendations.append("Ajoutez un sentiment d'urgence ou de rareté")
            
        # Émotion
        if features['emotion_score'] < 0.1:
            recommendations.append("Renforcez l'impact émotionnel")
            
        return recommendations