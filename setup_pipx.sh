#!/bin/bash

echo "🚀 Configuration avec pipx (méthode alternative)"
echo "=============================================="
echo ""

# Vérifier pipx
if ! command -v pipx &> /dev/null; then
    echo "⚠️  pipx n'est pas installé"
    echo ""
    echo "Pour installer pipx :"
    echo "  sudo apt update"
    echo "  sudo apt install pipx"
    echo "  pipx ensurepath"
    echo ""
    echo "Puis relancez ce script."
    exit 1
fi

echo "✓ pipx trouvé"

# Installer les outils principaux avec pipx
echo ""
echo "📦 Installation des outils avec pipx..."

# Streamlit pour le dashboard
echo "Installing streamlit..."
pipx install streamlit

# Installer les dépendances Python localement avec --user
echo ""
echo "📦 Installation des dépendances Python..."
echo "Note: Utilisation de --user pour éviter les conflits système"

python3 -m pip install --user pandas numpy pyyaml openpyxl xlsxwriter plotly

echo ""
echo "✅ Configuration terminée !"
echo ""
echo "🎯 Pour utiliser :"
echo "  python3 demo_analyzer.py     # Démo sans ML"
echo "  streamlit run app.py         # Dashboard (après pipx)"
echo ""
echo "💡 Cette méthode évite les conflits avec le système"