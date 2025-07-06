# 🚀 Guide de Démarrage Rapide - Discover Analyzer

## ⚡ Méthode 1 : Sans Installation (Démo)

La façon la plus rapide de tester l'outil :

```bash
# Aucune installation requise !
python3 demo_analyzer.py
```

Cette version utilise uniquement les bibliothèques Python standard.

## 🔧 Méthode 2 : Installation avec Environnement Virtuel

### Option A : Script automatique
```bash
# Lance l'installation guidée
./install.sh

# Puis utilisez les scripts créés :
./run_demo.sh              # Démo
./run_analyzer.sh file.csv  # Analyse
./run_dashboard.sh          # Dashboard web
```

### Option B : Installation manuelle
```bash
# 1. Installer python3-venv si nécessaire
sudo apt install python3.12-venv

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Installer les dépendances
pip install -r requirements_minimal.txt
```

## 🐳 Méthode 3 : Docker (Recommandé)

Pas de conflit avec votre système :

```bash
# Construire et lancer avec docker-compose
docker-compose up

# Ouvrir http://localhost:8501
```

Ou directement avec Docker :

```bash
# Construire l'image
docker build -t discover-analyzer .

# Lancer le container
docker run -p 8501:8501 -v $(pwd)/data:/app/data discover-analyzer
```

## 📦 Méthode 4 : Installation avec pipx

Pour éviter l'erreur "externally-managed-environment" :

```bash
# 1. Installer pipx si nécessaire
sudo apt install pipx
pipx ensurepath

# 2. Lancer le script
./setup_pipx.sh

# 3. Utiliser les outils
python3 demo_analyzer.py
streamlit run app.py
```

## 🎯 Utilisation Rapide

### Tester avec le fichier exemple
```bash
# La démo analyse automatiquement data/exemple_titres.csv
python3 demo_analyzer.py
```

### Analyser votre propre fichier
```bash
# Version simple (sans ML)
python3 demo_analyzer.py

# Version complète (nécessite installation)
python main.py votre_fichier.csv --title-column "Title"
```

### Format du CSV attendu
```csv
Title,Source,Date
"5 remèdes naturels contre le mal de dos","Site A","2024-01-01"
"Comment perdre du poids rapidement","Site B","2024-01-02"
```

## 🆘 Résolution des Problèmes

### Erreur "externally-managed-environment"
→ Utilisez une des méthodes ci-dessus (venv, Docker, ou pipx)

### Erreur "module not found"
→ Vérifiez que l'environnement virtuel est activé

### Erreur de mémoire
→ Utilisez `--max-titles 1000` pour limiter l'analyse

## 📊 Résultats

Les résultats sont sauvegardés dans :
- `exports/demo_results.json` (démo)
- `exports/classified_titles_*.csv` (analyse complète)
- `exports/patterns_insights_*.json` (patterns détectés)

## 💡 Conseil

Commencez par la **Méthode 1** (démo sans installation) pour tester rapidement l'outil !