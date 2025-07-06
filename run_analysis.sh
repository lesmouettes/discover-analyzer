#!/bin/bash
# Script de lancement rapide pour l'analyse

echo "🚀 Analyseur de Titres Google Discover"
echo "====================================="

# Vérifier si un fichier est fourni
if [ -z "$1" ]; then
    echo "❌ Erreur: Veuillez fournir un fichier CSV"
    echo "Usage: ./run_analysis.sh votre_fichier.csv [colonne_titres]"
    exit 1
fi

# Paramètres
INPUT_FILE="$1"
TITLE_COLUMN="${2:-Title}"
OUTPUT_DIR="exports/$(date +%Y%m%d_%H%M%S)"

# Vérifier que le fichier existe
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Erreur: Le fichier '$INPUT_FILE' n'existe pas"
    exit 1
fi

# Créer le dossier de sortie
mkdir -p "$OUTPUT_DIR"

echo ""
echo "📁 Fichier d'entrée: $INPUT_FILE"
echo "📊 Colonne des titres: $TITLE_COLUMN"
echo "📂 Dossier de sortie: $OUTPUT_DIR"
echo ""

# Lancer l'analyse
echo "⏳ Analyse en cours..."
python src/analyzer.py "$INPUT_FILE" \
    --column "$TITLE_COLUMN" \
    --output "$OUTPUT_DIR" \
    --batch-size 1000

# Vérifier le statut
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Analyse terminée avec succès!"
    echo "📁 Résultats disponibles dans: $OUTPUT_DIR"
    echo ""
    echo "📊 Pour visualiser les résultats dans le dashboard:"
    echo "   streamlit run src/streamlit_app.py"
else
    echo ""
    echo "❌ L'analyse a échoué. Vérifiez les logs ci-dessus."
    exit 1
fi