"""
Script pour vérifier et valider la classification des titres
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
import random

def verify_classification(csv_file, sample_size=50):
    """Vérifie la classification en montrant des exemples par catégorie"""
    
    print("🔍 VÉRIFICATION DE LA CLASSIFICATION")
    print("="*80)
    
    # Charger les résultats de classification
    with open('exports/demo_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Charger et classifier les titres
    from demo_analyzer import SimpleClassifier
    classifier = SimpleClassifier()
    
    titles_by_category = defaultdict(list)
    
    # Lire le CSV et classifier chaque titre
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Title' in row and row['Title']:
                title = row['Title']
                result = classifier.classify(title)
                category = result['category']
                titles_by_category[category].append({
                    'title': title,
                    'score': result['score'],
                    'confidence': result['confidence']
                })
    
    # Afficher des exemples pour chaque catégorie
    for category, titles in sorted(titles_by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{'='*80}")
        print(f"{category} - {len(titles)} titres ({len(titles)/len(titles_by_category)*100:.1f}%)")
        print(f"{'='*80}")
        
        # Trier par score de confiance
        titles_sorted = sorted(titles, key=lambda x: x['confidence'], reverse=True)
        
        # Afficher les 5 meilleurs et 5 moins bons
        print("\n✅ TOP 5 - Meilleure confiance :")
        for i, item in enumerate(titles_sorted[:5], 1):
            print(f"{i}. [{item['confidence']:.2f}] {item['title'][:100]}...")
            
        if len(titles) > 10:
            print("\n⚠️  BOTTOM 5 - Plus faible confiance (à vérifier) :")
            for i, item in enumerate(titles_sorted[-5:], 1):
                print(f"{i}. [{item['confidence']:.2f}] {item['title'][:100]}...")
        
        # Échantillon aléatoire
        if len(titles) > 15:
            print("\n🎲 5 EXEMPLES ALÉATOIRES :")
            sample = random.sample(titles[5:-5] if len(titles) > 10 else titles, min(5, len(titles)-10))
            for i, item in enumerate(sample, 1):
                print(f"{i}. [{item['confidence']:.2f}] {item['title'][:100]}...")
    
    # Analyser les erreurs potentielles
    print(f"\n\n{'='*80}")
    print("⚠️  ANALYSE DES CLASSIFICATIONS DOUTEUSES")
    print(f"{'='*80}")
    
    # Trouver les titres avec faible confiance
    all_titles = []
    for titles in titles_by_category.values():
        all_titles.extend(titles)
    
    low_confidence = [t for t in all_titles if t['confidence'] < 0.3]
    print(f"\nTitres avec confiance < 30% : {len(low_confidence)}")
    
    if low_confidence:
        print("\nExemples de classifications incertaines :")
        for item in sorted(low_confidence, key=lambda x: x['confidence'])[:10]:
            print(f"- [{item['confidence']:.2f}] {item['title'][:80]}...")
    
    # Statistiques de confiance
    confidences = [t['confidence'] for t in all_titles]
    avg_confidence = sum(confidences) / len(confidences)
    
    print(f"\n📊 STATISTIQUES DE CONFIANCE :")
    print(f"- Confiance moyenne : {avg_confidence:.2%}")
    print(f"- Titres haute confiance (>70%) : {len([c for c in confidences if c > 0.7])}")
    print(f"- Titres moyenne confiance (30-70%) : {len([c for c in confidences if 0.3 <= c <= 0.7])}")
    print(f"- Titres faible confiance (<30%) : {len([c for c in confidences if c < 0.3])}")
    
    # Suggestions d'amélioration
    print(f"\n💡 SUGGESTIONS D'AMÉLIORATION :")
    print("1. Vérifier manuellement les titres avec confiance < 30%")
    print("2. Ajouter des mots-clés spécifiques pour les catégories mal classées")
    print("3. Considérer une catégorie 'Autres' pour les titres ambigus")
    
    # Sauvegarder un fichier de vérification
    verification_file = Path('exports/verification_classification.csv')
    with open(verification_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Titre', 'Catégorie', 'Confiance', 'Score', 'À_Vérifier'])
        
        for cat, titles in titles_by_category.items():
            for item in sorted(titles, key=lambda x: x['confidence']):
                writer.writerow([
                    item['title'],
                    cat,
                    f"{item['confidence']:.2f}",
                    item['score'],
                    'OUI' if item['confidence'] < 0.3 else 'NON'
                ])
    
    print(f"\n✅ Fichier de vérification créé : {verification_file}")
    print("   (Triez par 'À_Vérifier' pour voir les classifications douteuses)")

def check_specific_category(csv_file, category_name):
    """Vérifie en détail une catégorie spécifique"""
    print(f"\n🔍 Analyse détaillée : {category_name}")
    print("="*60)
    
    from demo_analyzer import SimpleClassifier
    classifier = SimpleClassifier()
    
    matches = []
    misclassified = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Title' in row and row['Title']:
                title = row['Title']
                result = classifier.classify(title)
                
                if result['category'] == category_name:
                    matches.append((title, result['confidence']))
                elif category_name.lower() in title.lower():
                    # Titre qui devrait peut-être être dans cette catégorie
                    misclassified.append((title, result['category'], result['confidence']))
    
    print(f"\n✅ {len(matches)} titres classés dans {category_name}")
    print("\nExemples :")
    for title, conf in matches[:10]:
        print(f"- [{conf:.2f}] {title[:80]}...")
    
    if misclassified:
        print(f"\n⚠️  {len(misclassified)} titres potentiellement mal classés")
        print("(contiennent le mot-clé mais classés ailleurs)")
        for title, cat, conf in misclassified[:5]:
            print(f"- {title[:60]}... → {cat} [{conf:.2f}]")

if __name__ == "__main__":
    csv_file = "/home/whuzz/projets/patern/combined_cuisine_data.csv"
    
    # Vérification complète
    verify_classification(csv_file)
    
    # Vérifier spécifiquement la catégorie cuisine
    check_specific_category(csv_file, "🍽️ Recettes & Cuisine")