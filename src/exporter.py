"""
Module d'export des résultats dans différents formats
"""

import pandas as pd
import json
from pathlib import Path
import xlsxwriter
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    """Gestion des exports de données"""
    
    def export_to_excel(self, data: Dict, output_path: str):
        """Exporte les résultats dans un fichier Excel multi-onglets"""
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'align': 'center'
            })
            
            # 1. Onglet Vue d'ensemble
            overview_data = {
                'Métrique': [
                    'Total de titres analysés',
                    'Nombre de catégories',
                    'Titres haute confiance',
                    'Titres basse confiance',
                    'Titres multi-catégories'
                ],
                'Valeur': [
                    data.get('total_titles', 0),
                    len(data.get('distribution', {}).get('distribution', {})),
                    data.get('distribution', {}).get('high_confidence_titles', 0),
                    data.get('distribution', {}).get('low_confidence_titles', 0),
                    data.get('distribution', {}).get('multi_category_titles', 0)
                ]
            }
            df_overview = pd.DataFrame(overview_data)
            df_overview.to_excel(writer, sheet_name='Vue d\'ensemble', index=False)
            
            # 2. Onglet Distribution
            dist_data = data.get('distribution', {}).get('distribution_pct', {})
            if dist_data:
                df_dist = pd.DataFrame(
                    list(dist_data.items()),
                    columns=['Catégorie', 'Pourcentage']
                )
                df_dist.to_excel(writer, sheet_name='Distribution', index=False)
                
            # 3. Onglets par catégorie
            category_patterns = data.get('category_patterns', {})
            for category, patterns in category_patterns.items():
                # Limiter le nom de l'onglet à 31 caractères (limite Excel)
                sheet_name = category[:31]
                
                # Créer un DataFrame avec les infos de la catégorie
                cat_info = []
                cat_info.append(['Total titres', patterns.get('total_titles', 0)])
                cat_info.append(['Longueur moyenne', f"{patterns.get('avg_length', 0):.1f}"])
                
                # Top patterns
                if 'top_patterns' in patterns:
                    cat_info.append(['', ''])  # Ligne vide
                    cat_info.append(['TOP PATTERNS', ''])
                    for p in patterns['top_patterns']:
                        cat_info.append([p['type'], p['count']])
                        
                # Top mots
                if 'unique_words' in patterns:
                    cat_info.append(['', ''])
                    cat_info.append(['MOTS CLÉS', ''])
                    for i, word in enumerate(patterns['unique_words'][:10]):
                        cat_info.append([f"Mot {i+1}", word])
                        
                df_cat = pd.DataFrame(cat_info, columns=['Métrique', 'Valeur'])
                df_cat.to_excel(writer, sheet_name=sheet_name, index=False)
                
        logger.info(f"✓ Export Excel: {output_path}")
        
    def export_to_json_api(self, data: Dict, output_path: str):
        """Exporte au format JSON optimisé pour API"""
        
        api_data = {
            'metadata': {
                'total_titles': data.get('total_titles', 0),
                'analysis_date': data.get('analysis_date', ''),
                'categories_count': len(data.get('distribution', {}).get('distribution', {}))
            },
            'distribution': data.get('distribution', {}),
            'insights': data.get('insights', {}),
            'patterns_by_category': {}
        }
        
        # Simplifier les patterns pour l'API
        for cat, patterns in data.get('category_patterns', {}).items():
            api_data['patterns_by_category'][cat] = {
                'total': patterns.get('total_titles', 0),
                'avg_length': patterns.get('avg_length', 0),
                'top_patterns': [
                    {'type': p['type'], 'count': p['count']} 
                    for p in patterns.get('top_patterns', [])[:3]
                ],
                'keywords': patterns.get('unique_words', [])[:10]
            }
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"✓ Export JSON API: {output_path}")
        
    def generate_templates(self, insights: Dict, output_dir: str):
        """Génère des templates de titres par catégorie"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for category, cat_insights in insights.items():
            template_file = output_path / f"templates_{category.lower().replace(' ', '_')}.txt"
            
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(f"TEMPLATES DE TITRES - {category.upper()}\n")
                f.write("="*50 + "\n\n")
                
                # Insights
                f.write("CONSEILS D'OPTIMISATION:\n")
                for insight in cat_insights:
                    f.write(f"• {insight}\n")
                    
                f.write("\n" + "-"*50 + "\n\n")
                
                # Templates basés sur les insights
                f.write("TEMPLATES RECOMMANDÉS:\n\n")
                
                # Générer quelques templates types
                templates = self._generate_category_templates(category, cat_insights)
                for i, template in enumerate(templates, 1):
                    f.write(f"{i}. {template}\n")
                    
        logger.info(f"✓ Templates générés dans: {output_path}")
        
    def _generate_category_templates(self, category: str, insights: List[str]) -> List[str]:
        """Génère des templates spécifiques par catégorie"""
        
        templates = []
        
        # Templates génériques adaptables
        base_templates = [
            "[Nombre] [Sujet] qui [Bénéfice] [Timing optionnel]",
            "Comment [Action] : [Méthode] [Résultat]",
            "[Question] ? La réponse des [Experts]",
            "Le secret de [Groupe/Personne] pour [Objectif]",
            "[Découverte/Alerte] : [Information importante]"
        ]
        
        # Adapter selon la catégorie
        category_lower = category.lower()
        
        if 'santé' in category_lower:
            templates.extend([
                "5 remèdes naturels contre [problème] validés par la science",
                "Cette plante méconnue soulage [symptôme] en 7 jours",
                "Médecins : arrêtez [mauvaise habitude] immédiatement"
            ])
        elif 'sport' in category_lower or 'fitness' in category_lower:
            templates.extend([
                "Cet exercice brûle 300 calories en 15 minutes",
                "Programme : [objectif] en 30 jours sans équipement",
                "L'erreur fatale que 90% font à la salle"
            ])
        elif 'beauté' in category_lower:
            templates.extend([
                "Cette crème à 10€ remplace le botox selon les dermatologues",
                "Routine anti-âge : -10 ans en 3 semaines",
                "Le secret beauté des Coréennes enfin révélé"
            ])
        elif 'finance' in category_lower:
            templates.extend([
                "Comment j'ai économisé 10000€ en 6 mois avec cette méthode",
                "Les 3 investissements qui rapportent 15% par an",
                "Retraite : cette astuce peut doubler votre pension"
            ])
        elif 'cuisine' in category_lower or 'recette' in category_lower:
            templates.extend([
                "Recette : [plat] prêt en 20 minutes avec 3 ingrédients",
                "Le [plat] qui fait fureur sur TikTok (et c'est délicieux)",
                "Batch cooking : 7 repas sains préparés en 1 heure"
            ])
            
        # Ajouter les templates de base
        templates.extend(base_templates[:3])
        
        return templates[:8]  # Retourner max 8 templates