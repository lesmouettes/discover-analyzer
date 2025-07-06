"""
Rapport détaillé sur la précision de la classification
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

def analyze_classification_accuracy(csv_file):
    """Analyse la précision de la classification avec des métriques détaillées"""
    
    print("📊 RAPPORT DE CLASSIFICATION DÉTAILLÉ")
    print("="*80)
    
    from demo_analyzer import SimpleClassifier
    classifier = SimpleClassifier()
    
    # Analyser tous les titres
    all_classifications = []
    category_stats = defaultdict(lambda: {'total': 0, 'high_conf': 0, 'low_conf': 0, 'keywords_found': []})
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Title' in row and row['Title']:
                title = row['Title']
                result = classifier.classify(title)
                
                all_classifications.append({
                    'title': title,
                    'category': result['category'],
                    'confidence': result['confidence'],
                    'score': result['score']
                })
                
                # Stats par catégorie
                cat = result['category']
                category_stats[cat]['total'] += 1
                
                if result['confidence'] > 0.7:
                    category_stats[cat]['high_conf'] += 1
                elif result['confidence'] < 0.3:
                    category_stats[cat]['low_conf'] += 1
    
    # Analyser les résultats
    total_titles = len(all_classifications)
    
    print(f"\n📈 RÉSUMÉ GLOBAL")
    print(f"Total de titres analysés : {total_titles}")
    print(f"Catégories détectées : {len(category_stats)}")
    
    # Calculer la distribution réelle vs attendue
    print(f"\n📊 DISTRIBUTION PAR CATÉGORIE")
    print(f"{'Catégorie':<30} {'Total':>8} {'%':>6} {'Haute Conf':>10} {'Basse Conf':>10}")
    print("-"*70)
    
    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['total'], reverse=True):
        pct = (stats['total'] / total_titles) * 100
        print(f"{cat:<30} {stats['total']:>8} {pct:>6.1f}% {stats['high_conf']:>10} {stats['low_conf']:>10}")
    
    # Analyser les problèmes de classification
    print(f"\n⚠️  ANALYSE DES PROBLÈMES POTENTIELS")
    
    # 1. Titres ambigus (mots-clés de plusieurs catégories)
    ambiguous_titles = []
    for item in all_classifications:
        title_lower = item['title'].lower()
        matching_categories = 0
        
        # Vérifier les mots-clés de chaque catégorie
        for cat_key, cat_data in classifier.categories.items():
            if any(keyword in title_lower for keyword in cat_data['keywords']):
                matching_categories += 1
        
        if matching_categories > 2:
            ambiguous_titles.append(item)
    
    print(f"\nTitres ambigus (mots-clés de >2 catégories) : {len(ambiguous_titles)}")
    if ambiguous_titles:
        print("Exemples :")
        for item in ambiguous_titles[:5]:
            print(f"  - {item['title'][:80]}... → {item['category']}")
    
    # 2. Vérifier la catégorie Cuisine spécifiquement
    print(f"\n🍽️  FOCUS SUR LA CATÉGORIE CUISINE")
    
    cuisine_keywords = ['recette', 'cuisine', 'plat', 'cuire', 'cuisson', 'préparer', 
                       'ingrédient', 'repas', 'menu', 'gastronomie', 'chef', 'dessert',
                       'tarte', 'gâteau', 'gratin', 'soupe', 'salade']
    
    correctly_classified = 0
    misclassified = []
    
    for item in all_classifications:
        title_lower = item['title'].lower()
        has_cuisine_keyword = any(kw in title_lower for kw in cuisine_keywords)
        is_classified_cuisine = '🍽️ Recettes & Cuisine' in item['category']
        
        if has_cuisine_keyword and is_classified_cuisine:
            correctly_classified += 1
        elif has_cuisine_keyword and not is_classified_cuisine:
            misclassified.append(item)
    
    print(f"Titres avec mots-clés cuisine correctement classés : {correctly_classified}")
    print(f"Titres avec mots-clés cuisine mal classés : {len(misclassified)}")
    
    if misclassified:
        print("\nExemples de classifications à revoir :")
        for item in misclassified[:10]:
            print(f"  - '{item['title'][:60]}...' → {item['category']} [{item['confidence']:.2f}]")
    
    # 3. Créer un fichier CSV pour révision manuelle
    output_file = Path('exports/classification_review.csv')
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Titre', 'Catégorie_Assignée', 'Confiance', 'Mots_Clés_Cuisine', 'Révision_Suggérée'])
        
        for item in all_classifications:
            title_lower = item['title'].lower()
            has_cuisine_kw = any(kw in title_lower for kw in cuisine_keywords)
            
            # Suggérer une révision si :
            # 1. Faible confiance
            # 2. Mots-clés cuisine mais pas classé cuisine
            # 3. Titre ambigu
            
            needs_review = (
                item['confidence'] < 0.3 or
                (has_cuisine_kw and '🍽️ Recettes & Cuisine' not in item['category']) or
                item in ambiguous_titles
            )
            
            writer.writerow([
                item['title'],
                item['category'],
                f"{item['confidence']:.2f}",
                'OUI' if has_cuisine_kw else 'NON',
                'RÉVISER' if needs_review else 'OK'
            ])
    
    print(f"\n✅ Fichier de révision créé : {output_file}")
    print("   Filtrez par 'RÉVISER' pour voir les classifications à vérifier")
    
    # 4. Recommandations
    print(f"\n💡 RECOMMANDATIONS POUR AMÉLIORER LA CLASSIFICATION")
    print("1. Ajouter plus de mots-clés spécifiques pour chaque catégorie")
    print("2. Utiliser un système de pondération pour les mots-clés")
    print("3. Implémenter une catégorie 'Autres' pour les titres ambigus")
    print("4. Considérer le contexte (source du titre) pour améliorer la précision")
    
    return all_classifications

if __name__ == "__main__":
    csv_file = "/home/whuzz/projets/patern/combined_cuisine_data.csv"
    results = analyze_classification_accuracy(csv_file)