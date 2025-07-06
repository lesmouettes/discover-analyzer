#!/bin/bash

echo "🌐 Ouverture du rapport d'analyse..."
echo ""

# Chemin complet du fichier
REPORT_FILE="$(pwd)/exports/rapport_analyse_cuisine.html"

if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ Rapport non trouvé : $REPORT_FILE"
    echo "Lancez d'abord une analyse pour générer le rapport."
    exit 1
fi

echo "📁 Fichier : $REPORT_FILE"
echo ""

# Détecter le système et ouvrir avec le bon navigateur
if command -v xdg-open > /dev/null; then
    # Linux
    echo "Ouverture avec le navigateur par défaut..."
    xdg-open "$REPORT_FILE"
elif command -v open > /dev/null; then
    # macOS
    open "$REPORT_FILE"
elif command -v start > /dev/null; then
    # Windows
    start "$REPORT_FILE"
else
    # Alternative : afficher le chemin complet
    echo "🔗 Ouvrez ce lien dans votre navigateur :"
    echo "file://$REPORT_FILE"
    echo ""
    echo "Ou lancez un serveur local :"
    echo "python3 -m http.server 8000"
    echo "Puis ouvrez : http://localhost:8000/exports/rapport_analyse_cuisine.html"
fi