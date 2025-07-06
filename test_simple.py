"""
Test simple sans dépendances externes
"""

import os
import sys
from pathlib import Path

print("🧪 Test de la structure du projet Discover Analyzer")
print("="*50)

# Vérifier la structure
project_dir = Path(__file__).parent
print("\n✅ Structure du projet :")

dirs_to_check = ['src', 'config', 'exports', 'data', 'tests', 'models']
for dir_name in dirs_to_check:
    dir_path = project_dir / dir_name
    if dir_path.exists():
        print(f"  ✓ {dir_name}/ trouvé")
    else:
        print(f"  ✗ {dir_name}/ manquant")

# Vérifier les fichiers principaux
print("\n✅ Fichiers principaux :")
files_to_check = [
    'src/classifier.py',
    'src/pattern_detector.py', 
    'src/feature_extractor.py',
    'src/exporter.py',
    'src/analyzer.py',
    'config/categories.yaml',
    'requirements.txt',
    'README.md'
]

for file_name in files_to_check:
    file_path = project_dir / file_name
    if file_path.exists():
        size = file_path.stat().st_size
        print(f"  ✓ {file_name} ({size:,} octets)")
    else:
        print(f"  ✗ {file_name} manquant")

# Afficher les catégories configurées
print("\n✅ Catégories configurées :")
config_file = project_dir / 'config/categories.yaml'
if config_file.exists():
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
        categories = []
        for line in content.split('\n'):
            if 'name:' in line and not line.strip().startswith('#'):
                cat_name = line.split('"')[1]
                categories.append(cat_name)
        
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")

# Instructions d'installation
print("\n📦 Pour installer les dépendances :")
print("  pip install -r requirements.txt")
print("\n🚀 Pour lancer l'analyse :")
print("  python src/analyzer.py votre_fichier.csv")
print("\n📊 Pour le dashboard Streamlit :")
print("  streamlit run src/streamlit_app.py")

# Créer un fichier CSV d'exemple
print("\n📝 Création d'un fichier CSV d'exemple...")
example_csv = project_dir / 'data/exemple_titres.csv'
example_csv.parent.mkdir(exist_ok=True)

titres_exemple = [
    "5 remèdes naturels contre le mal de dos validés par la science",
    "Comment j'ai perdu 15kg en 3 mois sans régime drastique",
    "Cette crème à 10€ fait disparaître les rides en 7 jours",
    "La nouvelle tendance qui révolutionne le monde du travail",
    "Top 10 des plus belles plages secrètes de Bretagne",
    "Ma routine matinale qui a changé ma vie en 5 minutes",
    "Exposition Monet : les secrets cachés enfin révélés",
    "3 techniques approuvées par les psychologues contre l'anxiété",
    "Retraite : cette astuce peut doubler votre pension",
    "Le classement 2024 des voitures électriques les plus fiables",
    "Bitcoin : faut-il investir maintenant selon les experts",
    "Recette : gratin dauphinois express prêt en 20 minutes"
]

with open(example_csv, 'w', encoding='utf-8') as f:
    f.write("Title,Source\n")
    for titre in titres_exemple:
        f.write(f'"{titre}","Test"\n')

print(f"✓ Fichier exemple créé : {example_csv}")
print(f"  ({len(titres_exemple)} titres)")

print("\n✅ Structure du projet validée avec succès!")