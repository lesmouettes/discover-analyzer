"""
Script principal d'analyse - version optimisée
"""

import pandas as pd
import argparse
import logging
from pathlib import Path
import json
import sys
from datetime import datetime

# Import des modules
from classifier import DiscoverClassifier
from pattern_detector import PatternDetector
from feature_extractor import FeatureExtractor
from exporter import DataExporter

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DiscoverAnalyzer:
    """Analyseur principal pour les titres Google Discover"""
    
    def __init__(self):
        logger.info("Initialisation de l'analyseur...")
        self.classifier = DiscoverClassifier()
        self.pattern_detector = PatternDetector()
        self.feature_extractor = FeatureExtractor()
        self.exporter = DataExporter()
        
    def analyze_file(self, 
                    input_path: str, 
                    title_column: str = 'Title',
                    output_dir: str = 'exports',
                    batch_size: int = 1000):
        """
        Analyse un fichier CSV de titres
        
        Args:
            input_path: Chemin du fichier CSV
            title_column: Nom de la colonne contenant les titres
            output_dir: Dossier de sortie pour les exports
            batch_size: Taille des batchs pour traitement
        """
        # Créer le dossier de sortie
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Timestamp pour les fichiers
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 1. Charger les données
            logger.info(f"Chargement du fichier {input_path}...")
            df = pd.read_csv(input_path)
            total_titles = len(df)
            logger.info(f"✓ {total_titles} titres chargés")
            
            if title_column not in df.columns:
                raise ValueError(f"Colonne '{title_column}' non trouvée")
                
            # 2. Classification
            logger.info("Classification des titres...")
            titles = df[title_column].tolist()
            
            # Traiter par batch pour éviter les timeouts
            all_results = []
            for i in range(0, len(titles), batch_size):
                batch = titles[i:i+batch_size]
                logger.info(f"Traitement batch {i//batch_size + 1}/{(len(titles)-1)//batch_size + 1}")
                batch_results = self.classifier.classify_batch(batch)
                all_results.append(batch_results)
                
            df_classified = pd.concat(all_results, ignore_index=True)
            logger.info("✓ Classification terminée")
            
            # 3. Analyse de distribution
            distribution = self.classifier.analyze_distribution(df_classified)
            
            # 4. Détection de patterns par catégorie
            logger.info("Détection des patterns...")
            category_patterns = self.pattern_detector.analyze_patterns_by_category(df_classified)
            logger.info("✓ Patterns détectés")
            
            # 5. Extraction de features (sur échantillon pour performance)
            logger.info("Extraction des features linguistiques...")
            sample_size = min(5000, len(titles))
            sample_titles = titles[:sample_size]
            df_features = self.feature_extractor.extract_batch_features(sample_titles)
            logger.info("✓ Features extraites")
            
            # 6. Génération des insights
            logger.info("Génération des insights...")
            insights = self.pattern_detector.generate_pattern_insights(category_patterns)
            
            # 7. Export des résultats
            logger.info("Export des résultats...")
            
            # CSV principal avec classification
            output_csv = output_path / f"classified_titles_{timestamp}.csv"
            df_final = pd.concat([df, df_classified], axis=1)
            df_final.to_csv(output_csv, index=False)
            logger.info(f"✓ CSV exporté: {output_csv}")
            
            # JSON avec patterns et insights
            output_json = output_path / f"patterns_insights_{timestamp}.json"
            export_data = {
                'analysis_date': timestamp,
                'total_titles': total_titles,
                'distribution': distribution,
                'category_patterns': category_patterns,
                'insights': insights,
                'feature_stats': self.feature_extractor.analyze_feature_importance(df_features)
            }
            
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"✓ JSON exporté: {output_json}")
            
            # Rapport résumé
            self._generate_summary_report(
                distribution, 
                category_patterns, 
                insights,
                output_path / f"rapport_analyse_{timestamp}.txt"
            )
            
            logger.info("\n✅ Analyse complète terminée!")
            logger.info(f"📁 Résultats dans: {output_path}")
            
            return {
                'success': True,
                'output_dir': str(output_path),
                'files': {
                    'csv': str(output_csv),
                    'json': str(output_json)
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _generate_summary_report(self, distribution, patterns, insights, output_path):
        """Génère un rapport textuel de synthèse"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT D'ANALYSE - TITRES GOOGLE DISCOVER\n")
            f.write("="*80 + "\n\n")
            
            # Distribution
            f.write("1. DISTRIBUTION PAR CATÉGORIE\n")
            f.write("-"*40 + "\n")
            for cat, pct in distribution['distribution_pct'].items():
                f.write(f"  • {cat}: {pct}%\n")
            f.write(f"\nTitres haute confiance: {distribution['high_confidence_titles']}\n")
            f.write(f"Titres multi-catégories: {distribution['multi_category_titles']}\n\n")
            
            # Insights par catégorie
            f.write("2. INSIGHTS PAR CATÉGORIE\n")
            f.write("-"*40 + "\n")
            for cat, cat_insights in insights.items():
                f.write(f"\n{cat}:\n")
                for insight in cat_insights:
                    f.write(f"  - {insight}\n")
                    
            # Top patterns globaux
            f.write("\n3. TOP PATTERNS DÉTECTÉS\n")
            f.write("-"*40 + "\n")
            all_patterns = {}
            for cat_data in patterns.values():
                for pattern in cat_data.get('top_patterns', []):
                    pattern_type = pattern['type']
                    if pattern_type not in all_patterns:
                        all_patterns[pattern_type] = 0
                    all_patterns[pattern_type] += pattern['count']
                    
            top_global = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
            for pattern, count in top_global:
                f.write(f"  • {pattern}: {count} occurrences\n")
                
        logger.info(f"✓ Rapport généré: {output_path}")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='Analyseur de titres Google Discover')
    parser.add_argument('input_file', help='Fichier CSV d'entrée')
    parser.add_argument('--column', default='Title', help='Nom de la colonne des titres')
    parser.add_argument('--output', default='exports', help='Dossier de sortie')
    parser.add_argument('--batch-size', type=int, default=1000, help='Taille des batchs')
    
    args = parser.parse_args()
    
    # Lancer l'analyse
    analyzer = DiscoverAnalyzer()
    result = analyzer.analyze_file(
        args.input_file,
        title_column=args.column,
        output_dir=args.output,
        batch_size=args.batch_size
    )
    
    if result['success']:
        print("\n✅ Analyse terminée avec succès!")
        print(f"📁 Résultats dans: {result['output_dir']}")
    else:
        print(f"\n❌ Erreur: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()