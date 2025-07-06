"""
Analyse approfondie des patterns pour les titres de cuisine
"""

import csv
import re
from collections import Counter
from pathlib import Path

def analyze_cuisine_patterns(file_path):
    """Analyse spécifique des patterns de titres cuisine"""
    
    print(f"\n🍳 Analyse approfondie des patterns cuisine")
    print("="*60)
    
    # Lire les titres
    titles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Title' in row and row['Title']:
                titles.append(row['Title'])
    
    # Patterns spécifiques cuisine
    patterns = {
        'recette_de': [],
        'temps_preparation': [],
        'sans_ingredient': [],
        'facile_rapide': [],
        'menu_semaine': [],
        'ingredient_star': [],
        'technique_cuisine': [],
        'occasion_speciale': []
    }
    
    # Analyser chaque titre
    for title in titles:
        title_lower = title.lower()
        
        # Recette de X
        if re.search(r'recette(s)?\s+(de|du|des|d\')', title_lower):
            patterns['recette_de'].append(title)
            
        # Temps de préparation
        if re.search(r'\d+\s*(minutes?|mn|heures?|h)', title_lower):
            patterns['temps_preparation'].append(title)
            
        # Sans ingrédient (sans gluten, sans lactose, etc.)
        if re.search(r'\bsans\s+\w+', title_lower):
            patterns['sans_ingredient'].append(title)
            
        # Facile/Rapide
        if any(word in title_lower for word in ['facile', 'rapide', 'express', 'simple']):
            patterns['facile_rapide'].append(title)
            
        # Menu de la semaine
        if 'menu' in title_lower and 'semaine' in title_lower:
            patterns['menu_semaine'].append(title)
            
        # Ingrédient principal
        ingredients = ['chocolat', 'fraise', 'tomate', 'poulet', 'saumon', 'fromage', 'pomme']
        for ing in ingredients:
            if ing in title_lower:
                patterns['ingredient_star'].append(title)
                break
                
        # Technique de cuisine
        if any(tech in title_lower for tech in ['gratin', 'tarte', 'gâteau', 'rôti', 'sauté', 'glacé']):
            patterns['technique_cuisine'].append(title)
            
        # Occasion spéciale
        if any(occ in title_lower for occ in ['pâques', 'noël', 'fête', 'anniversaire', 'apéro']):
            patterns['occasion_speciale'].append(title)
    
    # Afficher les résultats
    print(f"\n📊 Patterns spécifiques cuisine détectés :\n")
    
    for pattern_name, examples in patterns.items():
        if examples:
            print(f"🔸 {pattern_name.replace('_', ' ').title()} : {len(examples)} occurrences ({len(examples)/len(titles)*100:.1f}%)")
            print(f"   Ex: {examples[0][:70]}...")
            print()
    
    # Analyse des formats de titres
    print("\n📝 Formats de titres les plus courants :")
    
    title_formats = {
        'Recette : [Plat]': 0,
        '[Plat] : la recette [Adjectif]': 0,
        '[Nombre] [Plats] pour [Occasion]': 0,
        'Comment [Action] [Plat]': 0,
        'Le/La [Plat] [Adjectif]': 0
    }
    
    for title in titles:
        if re.match(r'^Recette\s*:', title):
            title_formats['Recette : [Plat]'] += 1
        elif re.search(r':\s*la recette', title.lower()):
            title_formats['[Plat] : la recette [Adjectif]'] += 1
        elif re.match(r'^\d+.*pour', title):
            title_formats['[Nombre] [Plats] pour [Occasion]'] += 1
        elif title.lower().startswith('comment'):
            title_formats['Comment [Action] [Plat]'] += 1
        elif re.match(r'^(Le|La|Les)\s+\w+\s+\w+$', title):
            title_formats['Le/La [Plat] [Adjectif]'] += 1
    
    for format_name, count in sorted(title_formats.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  • {format_name}: {count} ({count/len(titles)*100:.1f}%)")
    
    # Mots déclencheurs cuisine
    print("\n🎯 Top 15 mots déclencheurs cuisine :")
    
    trigger_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        trigger_words.extend([w for w in words if len(w) > 4])
    
    word_counts = Counter(trigger_words)
    # Exclure les mots trop communs
    exclude = {'cette', 'votre', 'pour', 'avec', 'dans', 'plus', 'sans', 'tout', 'faire', 'vous'}
    
    cuisine_words = [(w, c) for w, c in word_counts.most_common(50) if w not in exclude][:15]
    
    for word, count in cuisine_words:
        print(f"  • {word}: {count} ({count/len(titles)*100:.1f}%)")
    
    # Templates recommandés
    print("\n💡 Templates haute performance pour titres cuisine :")
    print("  1. Recette : [Plat] [Adjectif] en [Temps] minutes")
    print("  2. [Nombre] [Recettes/Idées] de [Plat] pour [Occasion]") 
    print("  3. [Plat] : la recette [Adjectif] et [Adjectif]")
    print("  4. Comment réussir [Plat] à tous les coups")
    print("  5. Menu de la semaine : [Nombre] idées [Adjectif]")

if __name__ == "__main__":
    file_path = Path("/home/whuzz/projets/patern/combined_cuisine_data.csv")
    if file_path.exists():
        analyze_cuisine_patterns(file_path)
    else:
        print("❌ Fichier non trouvé")