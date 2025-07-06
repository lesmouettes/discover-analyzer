"""
Version de démonstration de l'analyseur sans dépendances ML
"""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
import json

class SimpleClassifier:
    """Version simplifiée du classificateur basée uniquement sur les mots-clés"""
    
    def __init__(self):
        self.categories = {
            'SANTE_NATURELLE': {
                'name': '🏥 Santé Naturelle',
                'keywords': ['remède', 'naturel', 'santé', 'nutrition', 'bien-être', 'guérir', 'soin', 'mal', 'douleur', 'médecin', 'science']
            },
            'SPORT_FITNESS': {
                'name': '💪 Sport & Fitness',
                'keywords': ['sport', 'fitness', 'exercice', 'musculation', 'entraînement', 'cardio', 'perdre', 'poids', 'kg']
            },
            'BEAUTE_ANTIAGE': {
                'name': '🌸 Beauté Anti-âge',
                'keywords': ['beauté', 'anti-âge', 'peau', 'visage', 'rides', 'cosmétique', 'crème', 'sérum']
            },
            'SOCIETE_TENDANCES': {
                'name': '🏛️ Société & Tendances',
                'keywords': ['société', 'tendance', 'comportement', 'social', 'évolution', 'nouveau', 'révolutionne', 'monde']
            },
            'VOYAGES_DECOUVERTES': {
                'name': '🗺️ Voyages & Découvertes',
                'keywords': ['voyage', 'destination', 'tourisme', 'découverte', 'région', 'plage', 'vacances', 'ville']
            },
            'LIFESTYLE_BIENETRE': {
                'name': '🌿 Lifestyle & Bien-être',
                'keywords': ['lifestyle', 'routine', 'habitude', 'bien-être', 'vie', 'quotidien', 'matin', 'changé']
            },
            'CULTURE_PATRIMOINE': {
                'name': '🎨 Culture & Patrimoine',
                'keywords': ['culture', 'art', 'patrimoine', 'exposition', 'spectacle', 'musée', 'artiste']
            },
            'PSYCHOLOGIE_MENTAL': {
                'name': '🧠 Psychologie & Mental',
                'keywords': ['psychologie', 'mental', 'émotion', 'comportement', 'stress', 'anxiété', 'psychologue']
            },
            'SENIOR_VIEILLISSEMENT': {
                'name': '👴 Senior & Vieillissement',
                'keywords': ['senior', 'retraite', 'âge', 'vieillissement', '60+', 'pension']
            },
            'AUTOMOBILE_MOBILITE': {
                'name': '🚗 Automobile & Mobilité',
                'keywords': ['voiture', 'auto', 'conduite', 'véhicule', 'mobilité', 'électrique']
            },
            'FINANCE_INVESTISSEMENT': {
                'name': '💰 Finance & Investissement',
                'keywords': ['finance', 'investissement', 'épargne', 'argent', 'crypto', 'bitcoin', 'investir']
            },
            'RECETTES_CUISINE': {
                'name': '🍽️ Recettes & Cuisine',
                'keywords': ['recette', 'cuisine', 'plat', 'culinaire', 'food', 'ingrédient', 'repas', 'gratin', 'minutes']
            }
        }
    
    def classify(self, title):
        """Classifie un titre dans une catégorie"""
        title_lower = title.lower()
        scores = {}
        
        for cat_key, cat_data in self.categories.items():
            score = sum(1 for keyword in cat_data['keywords'] if keyword in title_lower)
            scores[cat_key] = score
        
        # Trouver la catégorie avec le meilleur score
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # Calculer la confiance (basique)
        total_keywords = sum(scores.values())
        confidence = best_score / total_keywords if total_keywords > 0 else 0
        
        return {
            'category': self.categories[best_category]['name'],
            'confidence': confidence,
            'score': best_score
        }

class SimplePatternDetector:
    """Détecteur de patterns simplifié"""
    
    def detect_patterns(self, titles):
        """Détecte les patterns dans une liste de titres"""
        patterns = {
            'starts_with_number': [],
            'has_question': [],
            'has_colon': [],
            'has_urgency': [],
            'has_personal': []
        }
        
        for title in titles:
            # Pattern numérique au début
            if re.match(r'^\d+', title):
                patterns['starts_with_number'].append(title)
            
            # Question
            if '?' in title or title.lower().startswith(('comment', 'pourquoi', 'quand')):
                patterns['has_question'].append(title)
            
            # Deux points
            if ':' in title:
                patterns['has_colon'].append(title)
            
            # Urgence
            if any(word in title.lower() for word in ['urgent', 'maintenant', 'vite', 'immédiat']):
                patterns['has_urgency'].append(title)
            
            # Personnel
            if any(word in title.lower() for word in ["j'ai", 'mon', 'ma', 'mes', 'je']):
                patterns['has_personal'].append(title)
        
        return patterns

def analyze_csv(file_path):
    """Analyse un fichier CSV de titres"""
    print(f"\n📊 Analyse du fichier : {file_path}")
    print("="*60)
    
    # Lire le CSV
    titles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Title' in row:
                titles.append(row['Title'])
    
    print(f"\n✓ {len(titles)} titres chargés")
    
    # Classification
    classifier = SimpleClassifier()
    categories_count = defaultdict(int)
    classified_titles = []
    
    print("\n🏷️ Classification des titres...")
    for title in titles:
        result = classifier.classify(title)
        categories_count[result['category']] += 1
        classified_titles.append({
            'title': title,
            'category': result['category'],
            'confidence': result['confidence']
        })
    
    # Afficher la distribution
    print("\n📊 Distribution par catégorie :")
    for category, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(titles)) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")
    
    # Détection de patterns
    detector = SimplePatternDetector()
    patterns = detector.detect_patterns(titles)
    
    print("\n🔍 Patterns détectés :")
    for pattern_name, examples in patterns.items():
        if examples:
            print(f"\n  • {pattern_name}: {len(examples)} occurrences")
            print(f"    Exemple: {examples[0][:60]}...")
    
    # Statistiques générales
    lengths = [len(title) for title in titles]
    avg_length = sum(lengths) / len(lengths)
    
    print("\n📈 Statistiques générales :")
    print(f"  • Longueur moyenne: {avg_length:.1f} caractères")
    print(f"  • Longueur min/max: {min(lengths)} / {max(lengths)}")
    
    # Mots les plus fréquents
    all_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend([w for w in words if len(w) > 3])
    
    word_counts = Counter(all_words)
    print("\n📝 Top 10 mots les plus fréquents :")
    for word, count in word_counts.most_common(10):
        print(f"  • {word}: {count}")
    
    # Sauvegarder les résultats
    output_file = Path('exports/demo_results.json')
    output_file.parent.mkdir(exist_ok=True)
    
    results = {
        'total_titles': len(titles),
        'distribution': dict(categories_count),
        'patterns_count': {k: len(v) for k, v in patterns.items()},
        'avg_length': avg_length,
        'top_words': dict(word_counts.most_common(20))
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Résultats sauvegardés dans : {output_file}")

if __name__ == "__main__":
    import sys
    
    # Vérifier si un fichier est passé en argument
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.exists():
            analyze_csv(file_path)
        else:
            print(f"❌ Fichier non trouvé : {file_path}")
    else:
        # Analyser le fichier exemple par défaut
        example_file = Path('data/exemple_titres.csv')
        if example_file.exists():
            analyze_csv(example_file)
        else:
            print("❌ Fichier exemple non trouvé. Lancez d'abord test_simple.py")