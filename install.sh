#!/bin/bash

echo "🚀 Installation de Discover Analyzer"
echo "==================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "✓ Python3 trouvé : $(python3 --version)"

# Installer python3-venv si nécessaire
echo ""
echo "📦 Vérification de python3-venv..."
if ! python3 -m venv --help &> /dev/null 2>&1; then
    echo "⚠️  python3-venv n'est pas installé"
    echo "Installation requise : sudo apt install python3.12-venv"
    echo ""
    read -p "Voulez-vous l'installer maintenant ? (o/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        sudo apt update && sudo apt install -y python3.12-venv python3-pip
    else
        echo "Installation annulée. Installez python3-venv manuellement."
        exit 1
    fi
fi

# Créer l'environnement virtuel
echo ""
echo "🔧 Création de l'environnement virtuel..."
if [ -d "venv" ]; then
    echo "⚠️  Un environnement virtuel existe déjà"
    read -p "Voulez-vous le recréer ? (o/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo ""
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo ""
echo "📦 Mise à jour de pip..."
python -m pip install --upgrade pip

# Choisir le type d'installation
echo ""
echo "Choisissez le type d'installation :"
echo "1) Installation minimale (sans ML, rapide)"
echo "2) Installation complète (avec ML, ~2GB)"
echo ""
read -p "Votre choix (1 ou 2) : " -n 1 -r
echo ""

if [[ $REPLY == "1" ]]; then
    echo "📦 Installation minimale..."
    pip install -r requirements_minimal.txt
else
    echo "📦 Installation complète..."
    pip install -r requirements.txt
    
    # Télécharger les ressources NLTK
    echo ""
    echo "📚 Téléchargement des ressources NLTK..."
    python -c "import nltk; nltk.download('punkt', quiet=True)"
fi

# Créer un script de lancement
echo ""
echo "🚀 Création des scripts de lancement..."

# Script pour la démo
cat > run_demo.sh << 'EOF'
#!/bin/bash
source venv/bin/activate 2>/dev/null || { echo "Erreur: environnement virtuel non trouvé"; exit 1; }
python demo_analyzer.py
EOF

# Script pour l'analyse complète
cat > run_analyzer.sh << 'EOF'
#!/bin/bash
source venv/bin/activate 2>/dev/null || { echo "Erreur: environnement virtuel non trouvé"; exit 1; }
if [ -z "$1" ]; then
    echo "Usage: ./run_analyzer.sh votre_fichier.csv"
    exit 1
fi
python main.py "$@"
EOF

# Script pour le dashboard
cat > run_dashboard.sh << 'EOF'
#!/bin/bash
source venv/bin/activate 2>/dev/null || { echo "Erreur: environnement virtuel non trouvé"; exit 1; }
echo "🌐 Lancement du dashboard sur http://localhost:8501"
streamlit run app.py
EOF

# Rendre les scripts exécutables
chmod +x run_demo.sh run_analyzer.sh run_dashboard.sh

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🎯 Pour commencer :"
echo "  ./run_demo.sh              # Lancer la démo"
echo "  ./run_analyzer.sh fichier.csv  # Analyser un fichier"
echo "  ./run_dashboard.sh         # Ouvrir le dashboard web"
echo ""
echo "💡 Conseil : Commencez par ./run_demo.sh pour tester"