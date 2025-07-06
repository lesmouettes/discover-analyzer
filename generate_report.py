"""
Générateur de rapport détaillé pour l'analyse
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def generate_detailed_report(csv_file, json_file, output_file):
    """Génère un rapport HTML détaillé avec graphiques"""
    
    # Charger les résultats JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Générer le HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse - Discover Analyzer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2E7D32;
            text-align: center;
            margin-bottom: 30px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
        }}
        .metric-label {{
            color: #666;
            margin-top: 5px;
        }}
        .chart {{
            margin-bottom: 40px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .pattern-box {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #1f77b4;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport d'Analyse - Titres Google Discover</h1>
        
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{results['total_titles']}</div>
                <div class="metric-label">Titres analysés</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{results['avg_length']:.0f}</div>
                <div class="metric-label">Longueur moyenne (car.)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(results['distribution'])}</div>
                <div class="metric-label">Catégories détectées</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{sum(results['patterns_count'].values())}</div>
                <div class="metric-label">Patterns trouvés</div>
            </div>
        </div>
        
        <h2>Distribution par Catégorie</h2>
        <div id="pieChart" class="chart"></div>
        
        <h2>Patterns Détectés</h2>
        <div id="barChart" class="chart"></div>
        
        <h2>Top 15 Mots-Clés</h2>
        <table>
            <thead>
                <tr>
                    <th>Mot</th>
                    <th>Occurrences</th>
                    <th>Fréquence</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Ajouter les mots-clés au tableau
    for word, count in list(results['top_words'].items())[:15]:
        freq = (count / results['total_titles']) * 100
        html_content += f"""
                <tr>
                    <td><strong>{word}</strong></td>
                    <td>{count}</td>
                    <td>{freq:.1f}%</td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
        
        <h2>Recommandations</h2>
        <div class="pattern-box">
            <h3>🎯 Patterns Gagnants Identifiés</h3>
            <ul>
                <li><strong>Structure avec deux-points</strong> : Utilisée dans 51% des titres</li>
                <li><strong>Personnalisation</strong> : 57% des titres utilisent "votre", "vos", etc.</li>
                <li><strong>Questions</strong> : Format "Comment..." présent dans 12% des titres</li>
                <li><strong>Listes numériques</strong> : 7% des titres commencent par un chiffre</li>
            </ul>
        </div>
        
        <div class="pattern-box">
            <h3>💡 Templates Recommandés</h3>
            <ol>
                <li>Recette : [Plat] [Adjectif] en [Temps] minutes</li>
                <li>[Nombre] [Recettes/Idées] de [Plat] pour [Occasion]</li>
                <li>[Plat] : la recette [Adjectif] et [Adjectif]</li>
                <li>Comment réussir [Plat] à tous les coups</li>
                <li>Menu de la semaine : [Nombre] idées [Adjectif]</li>
            </ol>
        </div>
        
        <p style="text-align: center; color: #666; margin-top: 40px;">
            Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        </p>
    </div>
    
    <script>
        // Graphique en secteurs
        var pieData = [{
            values: {list(results['distribution'].values())},
            labels: {list(results['distribution'].keys())},
            type: 'pie',
            textinfo: 'label+percent',
            textposition: 'outside'
        }];
        
        var pieLayout = {{
            title: 'Répartition des titres par catégorie',
            height: 500
        }};
        
        Plotly.newPlot('pieChart', pieData, pieLayout);
        
        // Graphique en barres
        var barData = [{{
            x: {list(results['patterns_count'].keys())},
            y: {list(results['patterns_count'].values())},
            type: 'bar',
            marker: {{
                color: '#1f77b4'
            }}
        }}];
        
        var barLayout = {{
            title: 'Nombre de titres par type de pattern',
            xaxis: {{ title: 'Type de pattern' }},
            yaxis: {{ title: 'Nombre de titres' }}
        }};
        
        Plotly.newPlot('barChart', barData, barLayout);
    </script>
</body>
</html>
"""
    
    # Sauvegarder le rapport HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Rapport HTML généré : {output_file}")

if __name__ == "__main__":
    # Générer le rapport
    generate_detailed_report(
        csv_file="/home/whuzz/projets/patern/combined_cuisine_data.csv",
        json_file="exports/demo_results.json",
        output_file="exports/rapport_analyse_cuisine.html"
    )