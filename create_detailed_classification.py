"""
Créer un fichier détaillé montrant chaque titre avec sa catégorie
"""

import csv
from demo_analyzer import SimpleClassifier
from pathlib import Path

def create_detailed_classification_file(input_csv, output_dir="exports"):
    """Crée plusieurs fichiers pour visualiser facilement la classification"""
    
    print("📝 Création des fichiers de classification détaillés...")
    
    classifier = SimpleClassifier()
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 1. Fichier complet avec tous les titres et leurs catégories
    all_titles_file = output_path / "classification_complete.csv"
    
    # 2. Un fichier par catégorie
    titles_by_category = {}
    
    # Lire et classifier tous les titres
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        with open(all_titles_file, 'w', encoding='utf-8', newline='') as out_f:
            writer = csv.writer(out_f)
            writer.writerow(['Numéro', 'Titre', 'Catégorie', 'Confiance', 'Score'])
            
            row_num = 1
            for row in reader:
                if 'Title' in row and row['Title']:
                    title = row['Title']
                    result = classifier.classify(title)
                    category = result['category']
                    
                    # Écrire dans le fichier complet
                    writer.writerow([
                        row_num,
                        title,
                        category,
                        f"{result['confidence']:.2f}",
                        result['score']
                    ])
                    
                    # Stocker pour les fichiers par catégorie
                    if category not in titles_by_category:
                        titles_by_category[category] = []
                    
                    titles_by_category[category].append({
                        'num': row_num,
                        'title': title,
                        'confidence': result['confidence'],
                        'score': result['score']
                    })
                    
                    row_num += 1
    
    print(f"✅ Fichier complet créé : {all_titles_file}")
    print(f"   Total : {row_num-1} titres classifiés")
    
    # 2. Créer un fichier par catégorie
    category_files_dir = output_path / "par_categorie"
    category_files_dir.mkdir(exist_ok=True)
    
    for category, titles in titles_by_category.items():
        # Nettoyer le nom pour le fichier
        clean_name = category.replace('🏥', 'sante')\
                            .replace('💪', 'sport')\
                            .replace('🌸', 'beaute')\
                            .replace('🏛️', 'societe')\
                            .replace('🗺️', 'voyages')\
                            .replace('🌿', 'lifestyle')\
                            .replace('🎨', 'culture')\
                            .replace('🧠', 'psycho')\
                            .replace('👴', 'senior')\
                            .replace('🚗', 'auto')\
                            .replace('💰', 'finance')\
                            .replace('🍽️', 'cuisine')\
                            .replace(' ', '_').lower()
        
        filename = category_files_dir / f"{clean_name}.csv"
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Numéro', 'Titre', 'Confiance', 'Score'])
            
            # Trier par confiance décroissante
            sorted_titles = sorted(titles, key=lambda x: x['confidence'], reverse=True)
            
            for item in sorted_titles:
                writer.writerow([
                    item['num'],
                    item['title'],
                    f"{item['confidence']:.2f}",
                    item['score']
                ])
        
        print(f"   📁 {filename.name} : {len(titles)} titres")
    
    # 3. Créer un fichier résumé en TXT facile à lire
    summary_file = output_path / "classification_resume.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("CLASSIFICATION DÉTAILLÉE DES TITRES\n")
        f.write("="*100 + "\n\n")
        
        for category, titles in sorted(titles_by_category.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"\n{category} ({len(titles)} titres)\n")
            f.write("-"*80 + "\n")
            
            # Montrer les 10 premiers et 5 derniers
            sorted_titles = sorted(titles, key=lambda x: x['confidence'], reverse=True)
            
            f.write("\nMEILLEURES CLASSIFICATIONS (Top 10) :\n")
            for i, item in enumerate(sorted_titles[:10], 1):
                f.write(f"{i:3d}. [{item['confidence']:.2f}] {item['title'][:100]}\n")
            
            if len(titles) > 15:
                f.write("\n...\n")
                f.write("\nCLASSIFICATIONS LES PLUS FAIBLES (Bottom 5) :\n")
                for i, item in enumerate(sorted_titles[-5:], 1):
                    f.write(f"{i:3d}. [{item['confidence']:.2f}] {item['title'][:100]}\n")
            
            f.write("\n")
    
    print(f"\n✅ Fichier résumé créé : {summary_file}")
    
    # 4. Créer un index HTML pour navigation facile
    index_file = output_path / "index_classification.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Classification des Titres - Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2E7D32; }
        .category { 
            background: #f5f5f5; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px;
            border-left: 5px solid #2E7D32;
        }
        .stats { color: #666; font-size: 0.9em; }
        a { color: #1976D2; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📊 Index de Classification des Titres</h1>
    
    <h2>📁 Fichiers disponibles :</h2>
    
    <div class="category">
        <h3>Vue complète</h3>
        <a href="classification_complete.csv">classification_complete.csv</a>
        <p class="stats">Tous les titres avec leurs catégories assignées</p>
    </div>
    
    <div class="category">
        <h3>Vue résumée</h3>
        <a href="classification_resume.txt">classification_resume.txt</a>
        <p class="stats">Résumé lisible avec exemples par catégorie</p>
    </div>
    
    <div class="category">
        <h3>Fichiers par catégorie</h3>
        <ul>
""")
        
        for category in sorted(titles_by_category.keys()):
            clean_name = category.replace('🏥', 'sante')\
                                .replace('💪', 'sport')\
                                .replace('🌸', 'beaute')\
                                .replace('🏛️', 'societe')\
                                .replace('🗺️', 'voyages')\
                                .replace('🌿', 'lifestyle')\
                                .replace('🎨', 'culture')\
                                .replace('🧠', 'psycho')\
                                .replace('👴', 'senior')\
                                .replace('🚗', 'auto')\
                                .replace('💰', 'finance')\
                                .replace('🍽️', 'cuisine')\
                                .replace(' ', '_').lower()
            
            count = len(titles_by_category[category])
            f.write(f'            <li><a href="par_categorie/{clean_name}.csv">{category}</a> <span class="stats">({count} titres)</span></li>\n')
        
        f.write("""
        </ul>
    </div>
    
    <p style="margin-top: 40px; color: #666;">
        Généré par Discover Analyzer
    </p>
</body>
</html>
""")
    
    print(f"✅ Index HTML créé : {index_file}")
    print("\n📊 RÉSUMÉ :")
    for cat, titles in sorted(titles_by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {cat}: {len(titles)} titres")

if __name__ == "__main__":
    csv_file = "/home/whuzz/projets/patern/combined_cuisine_data.csv"
    create_detailed_classification_file(csv_file)