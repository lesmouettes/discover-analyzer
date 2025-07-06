# 📦 Guide d'Installation - Discover Analyzer

## 🚀 Installation Rapide

### 1. Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- 2GB d'espace disque (pour les modèles NLP)

### 2. Installation des dépendances

```bash
# Se placer dans le dossier du projet
cd discover-analyzer

# Créer un environnement virtuel (recommandé)
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
# venv\Scripts\activate

# Installer toutes les dépendances
pip install -r requirements.txt

# Télécharger les ressources NLTK
python -c "import nltk; nltk.download('punkt')"
```

## 🧪 Test de l'Installation

### Version de démonstration (sans ML)
```bash
# Test simple sans dépendances lourdes
python3 demo_analyzer.py
```

### Version complète
```bash
# Une fois les dépendances installées
python test_analyzer.py
```

## 📊 Utilisation

### 1. Analyse en ligne de commande
```bash
# Analyse basique
python main.py votre_fichier.csv

# Avec options avancées
python main.py votre_fichier.csv \
    --title-column "Title" \
    --output-dir "mes_resultats" \
    --max-titles 5000 \
    --export-formats excel json
```

### 2. Dashboard interactif
```bash
# Lancer l'interface web
streamlit run app.py
```

### 3. Script rapide
```bash
# Utiliser le script shell
./run_analysis.sh votre_fichier.csv
```

## 🔧 Résolution des Problèmes

### Erreur "ModuleNotFoundError"
Si vous obtenez des erreurs de modules manquants :

1. Vérifiez que l'environnement virtuel est activé
2. Réinstallez les dépendances : `pip install -r requirements.txt --upgrade`

### Erreur avec sentence-transformers
Le téléchargement du modèle peut prendre du temps lors de la première utilisation.
Si vous avez des problèmes de connexion :

```bash
# Installer avec timeout plus long
pip install sentence-transformers --default-timeout=100
```

### Problèmes de mémoire
Pour les gros fichiers CSV, utilisez l'option `--max-titles` pour limiter le nombre de titres analysés :

```bash
python main.py gros_fichier.csv --max-titles 1000
```

## 📁 Format du CSV d'Entrée

Votre fichier CSV doit contenir au minimum une colonne avec les titres :

```csv
Title,Source,Date
"5 remèdes naturels contre le mal de dos","Site A","2024-01-01"
"Comment perdre du poids rapidement","Site B","2024-01-02"
```

## 🎯 Exemples d'Utilisation

### Analyse rapide avec export Excel
```bash
python main.py data/exemple_titres.csv --export-formats excel
```

### Analyse complète avec tous les exports
```bash
python main.py mon_fichier.csv \
    --title-column "Titre" \
    --output-dir "analyse_complete" \
    --export-formats excel json pdf csv
```

### Dashboard pour exploration interactive
```bash
streamlit run app.py
# Puis ouvrir http://localhost:8501
```

## 💡 Conseils

1. **Pour commencer** : Utilisez `demo_analyzer.py` pour tester rapidement
2. **Pour production** : Installez toutes les dépendances et utilisez `main.py`
3. **Pour exploration** : Utilisez le dashboard Streamlit
4. **Pour automatisation** : Utilisez le script `run_analysis.sh`

## 📞 Support

En cas de problème :
1. Vérifiez ce guide d'installation
2. Consultez le README.md
3. Lancez `python test_simple.py` pour vérifier la structure