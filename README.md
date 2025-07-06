# 🔍 Discover Analyzer - Analyseur de Titres Google Discover

Outil complet d'analyse de titres Google Discover avec classification automatique en 12 catégories, détection de patterns haute performance et génération d'insights actionnables.

## 🚀 Installation

```bash
# Cloner le projet
cd discover-analyzer

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les ressources NLTK (première fois seulement)
python -c "import nltk; nltk.download('punkt')"
```

## 📋 Utilisation

### 1. Ligne de commande

```bash
# Analyse basique
python main.py votre_fichier.csv

# Avec options
python main.py votre_fichier.csv \
    --title-column "Title" \
    --output-dir "resultats" \
    --max-titles 1000 \
    --export-formats excel json pdf csv
```

### 2. Dashboard interactif

```bash
# Lancer le dashboard Streamlit
streamlit run app.py
```

### 3. Utilisation programmatique

```python
from src.classifier import DiscoverClassifier
from src.pattern_detector import PatternDetector

# Classification
classifier = DiscoverClassifier()
result = classifier.classify_title("5 remèdes naturels contre le mal de dos")
print(f"Catégorie: {result['main_category_name']} (confiance: {result['confidence']:.2f})")

# Détection de patterns
detector = PatternDetector()
patterns = detector.detect_structures(titles_list)
```

## 📊 Fonctionnalités

### Classification automatique
- 12 catégories officielles Google Discover
- Modèle hybride : mots-clés + similarité sémantique
- Score de confiance pour chaque classification
- Support multi-catégories

### Détection de patterns exhaustive
- Patterns structurels (ouverture/fermeture)
- Patterns d'autorité et crédibilité
- Patterns émotionnels et psychologiques
- Patterns quantifiés et mesurables
- Patterns narratifs et storytelling
- Patterns saisonniers et temporels

### Analyse linguistique
- Extraction de 20+ features par titre
- Scores émotionnels et d'urgence
- Analyse de lisibilité
- Recommandations personnalisées

### Exports multiples
- **Excel** : Classification complète avec onglets par catégorie
- **JSON** : Format API-ready pour intégration
- **PDF** : Rapport visuel avec graphiques
- **CSV** : Templates réutilisables

## 🏷️ Les 12 Catégories

1. 🏥 **Santé Naturelle** - Remèdes, nutrition, bien-être
2. 💪 **Sport & Fitness** - Exercices, musculation, entraînement
3. 🌸 **Beauté Anti-âge** - Soins, cosmétiques, anti-rides
4. 🏛️ **Société & Tendances** - Comportements, évolutions sociales
5. 🗺️ **Voyages & Découvertes** - Destinations, tourisme
6. 🌿 **Lifestyle & Bien-être** - Routines, développement personnel
7. 🎨 **Culture & Patrimoine** - Arts, expositions, spectacles
8. 🧠 **Psychologie & Mental** - Émotions, comportement, stress
9. 👴 **Senior & Vieillissement** - Retraite, santé 60+
10. 🚗 **Automobile & Mobilité** - Voitures, conduite
11. 💰 **Finance & Investissement** - Épargne, crypto, immobilier
12. 🍽️ **Recettes & Cuisine** - Plats, gastronomie

## 📈 Dashboard Streamlit

Le dashboard interactif offre :
- Vue d'ensemble avec métriques clés
- Analyse détaillée par catégorie
- Visualisation des patterns détectés
- Graphiques interactifs
- Export en un clic

## 🛠️ Structure du projet

```
discover-analyzer/
├── src/
│   ├── classifier.py       # Module de classification
│   ├── pattern_detector.py # Détection de patterns
│   ├── feature_extractor.py # Extraction de features
│   └── exporter.py         # Export multi-formats
├── config/
│   └── categories.yaml     # Configuration des catégories
├── exports/               # Dossier des exports
├── app.py                # Dashboard Streamlit
├── main.py              # Script principal CLI
└── requirements.txt     # Dépendances
```

## 📊 Exemple de sortie

```
=== ANALYSE DE DISTRIBUTION ===
Total de titres: 1000
Titres haute confiance (>70%): 823 (82.3%)
Titres multi-catégories: 156 (15.6%)

=== DISTRIBUTION PAR CATÉGORIE ===
Santé Naturelle: 18.5%
Recettes & Cuisine: 15.2%
Beauté Anti-âge: 12.8%
Sport & Fitness: 10.4%
...

=== INSIGHTS PRINCIPAUX ===
Santé Naturelle :
  • Longueur optimale : 65 à 85 caractères
  • Pattern dominant : opening comment
  • Mots-clés performants : remède, naturel, santé, bien-être
```

## 🔧 Configuration avancée

Modifier `config/categories.yaml` pour :
- Ajouter/modifier des mots-clés
- Ajuster les catégories
- Personnaliser les seuils

## 📝 Licence

MIT License

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
- Reporter des bugs
- Proposer des améliorations
- Ajouter des patterns