"""
Script de test rapide de l'analyseur
"""

import sys
sys.path.append('src')

from classifier import DiscoverClassifier
from pattern_detector import PatternDetector
from feature_extractor import FeatureExtractor

# Titres de test
test_titles = [
    "5 remèdes naturels contre le mal de dos validés par la science",
    "Comment j'ai perdu 15kg en 3 mois sans régime drastique", 
    "Cette crème à 10€ fait disparaître les rides en 7 jours",
    "La nouvelle tendance qui révolutionne le monde du travail en 2024",
    "Top 10 des plus belles plages secrètes de Bretagne",
    "Ma routine matinale de 5 minutes qui a changé ma vie",
    "Exposition Monet : les secrets cachés enfin révélés",
    "Gérer son anxiété : 3 techniques approuvées par les psychologues",
    "Retraite à 60 ans : cette astuce peut doubler votre pension",
    "Voitures électriques : le classement 2024 des plus fiables",
    "Bitcoin : faut-il investir maintenant ? L'avis des experts",
    "Recette express : gratin dauphinois prêt en 20 minutes"
]

print("🧪 Test de l'analyseur Google Discover")
print("="*50)

# Test du classificateur
print("\n1. TEST DE CLASSIFICATION")
print("-"*30)

classifier = DiscoverClassifier()

for title in test_titles[:3]:
    result = classifier.classify_title(title)
    print(f"\n📝 {title}")
    print(f"   → {result['category_emoji']} {result['main_category_name']}")
    print(f"   → Confiance: {result['confidence']:.0%}")
    if result['secondary_categories']:
        print(f"   → Secondaire: {result['secondary_categories'][0][0]}")

# Test du détecteur de patterns
print("\n\n2. TEST DE DETECTION DE PATTERNS")
print("-"*30)

detector = PatternDetector()
structures = detector.detect_structures(test_titles)

print(f"\n📊 Patterns trouvés:")
for pattern_type, examples in list(structures.items())[:5]:
    print(f"\n• {pattern_type}: {len(examples)} occurrences")
    print(f"  Exemple: {examples[0][:60]}...")

# Test de l'extracteur de features
print("\n\n3. TEST D'EXTRACTION DE FEATURES")
print("-"*30)

extractor = FeatureExtractor()
features = extractor.extract_features(test_titles[0])

print(f"\n📐 Features du titre: '{test_titles[0][:50]}...'")
print(f"   • Longueur: {features['length']} caractères")
print(f"   • Mots: {features['word_count']}")
print(f"   • Mots puissants: {features['power_words_count']}")
print(f"   • Score émotionnel: {features['emotion_score']:.2f}")
print(f"   • Score urgence: {features['urgency_score']:.2f}")

# Recommandations
recommendations = extractor.get_feature_recommendations(features)
if recommendations:
    print(f"\n💡 Recommandations:")
    for rec in recommendations:
        print(f"   - {rec}")

print("\n\n✅ Tests terminés avec succès!")
print("\nPour une analyse complète, utilisez:")
print("  python src/analyzer.py votre_fichier.csv")
print("ou")
print("  streamlit run src/streamlit_app.py")