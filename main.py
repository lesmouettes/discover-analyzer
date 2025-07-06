#!/usr/bin/env python3
"""
Script principal pour l'analyse des titres Google Discover
"""

import argparse
import logging
from pathlib import Path
import pandas as pd
import sys

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent / 'src'))

from classifier import DiscoverClassifier, process_csv
from pattern_detector import PatternDetector
from feature_extractor import FeatureExtractor
from exporter import ResultExporter

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Analyseur de titres Google Discover"
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help="Fichier CSV contenant les titres à analyser"
    )
    
    parser.add_argument(
        '--title-column',
        type=str,
        default='Title',
        help="Nom de la colonne contenant les titres (défaut: 'Title')"
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='exports',
        help="Dossier de sortie pour les exports (défaut: 'exports')"
    )
    
    parser.add_argument(
        '--max-titles',
        type=int,
        default=None,
        help="Nombre maximum de titres à analyser (défaut: tous)"
    )
    
    parser.add_argument(
        '--export-formats',
        nargs='+',
        choices=['excel', 'json', 'pdf', 'csv'],
        default=['excel', 'json'],
        help="Formats d'export souhaités (défaut: excel json)"
    )
    
    args = parser.parse_args()
    
    # Vérifier que le fichier existe
    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Fichier non trouvé : {input_path}")
        sys.exit(1)
        
    try:
        # Charger les données
        logger.info(f"Chargement du fichier {input_path}")
        df = pd.read_csv(input_path)
        
        # Vérifier la colonne
        if args.title_column not in df.columns:
            logger.error(f"Colonne '{args.title_column}' non trouvée dans le CSV")
            logger.info(f"Colonnes disponibles : {', '.join(df.columns)}")
            sys.exit(1)
            
        # Limiter le nombre de titres si demandé
        if args.max_titles:
            df = df.head(args.max_titles)
            
        titles = df[args.title_column].dropna().tolist()
        logger.info(f"Nombre de titres à analyser : {len(titles)}")
        
        # 1. Classification
        logger.info("=== PHASE 1 : Classification ===")
        classifier = DiscoverClassifier()
        df_classified = classifier.classify_batch(titles)
        
        # Afficher la distribution
        distribution = classifier.analyze_distribution(df_classified)
        logger.info(f"Distribution des catégories :")
        for cat, pct in distribution['distribution_pct'].items():
            logger.info(f"  - {cat}: {pct}%")
            
        # 2. Détection de patterns
        logger.info("\n=== PHASE 2 : Détection de patterns ===")
        pattern_detector = PatternDetector()
        patterns_by_category = pattern_detector.analyze_patterns_by_category(df_classified)
        
        # 3. Extraction de features
        logger.info("\n=== PHASE 3 : Extraction de features ===")
        feature_extractor = FeatureExtractor()
        df_features = feature_extractor.extract_batch_features(titles)
        
        # 4. Génération d'insights
        logger.info("\n=== PHASE 4 : Génération d'insights ===")
        insights = pattern_detector.generate_pattern_insights(patterns_by_category)
        
        # 5. Export des résultats
        logger.info("\n=== PHASE 5 : Export des résultats ===")
        exporter = ResultExporter(args.output_dir)
        
        exported_files = []
        
        if 'excel' in args.export_formats:
            excel_path = exporter.export_to_excel(
                df_classified, patterns_by_category, insights
            )
            exported_files.append(excel_path)
            
        if 'json' in args.export_formats:
            json_path = exporter.export_to_json(
                df_classified, patterns_by_category, insights
            )
            exported_files.append(json_path)
            
        if 'pdf' in args.export_formats:
            pdf_path = exporter.export_to_pdf(
                df_classified, patterns_by_category, insights
            )
            exported_files.append(pdf_path)
            
        if 'csv' in args.export_formats:
            csv_path = exporter.export_templates_csv(patterns_by_category)
            exported_files.append(csv_path)
            
        # Résumé final
        logger.info("\n=== ANALYSE TERMINÉE ===")
        logger.info(f"Titres analysés : {len(titles)}")
        logger.info(f"Fichiers exportés :")
        for file in exported_files:
            logger.info(f"  - {file}")
            
        # Afficher quelques insights
        logger.info("\n=== INSIGHTS PRINCIPAUX ===")
        for i, (category, cat_insights) in enumerate(list(insights.items())[:3]):
            logger.info(f"\n{category} :")
            for insight in cat_insights[:2]:
                logger.info(f"  • {insight}")
                
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()