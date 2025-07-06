"""
Dashboard Streamlit pour l'analyse des titres Google Discover
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent / 'src'))

from classifier import DiscoverClassifier
from pattern_detector import PatternDetector
from feature_extractor import FeatureExtractor

# Configuration Streamlit
st.set_page_config(
    page_title="Discover Analyzer - Analyse de Titres",
    page_icon="📊",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .pattern-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Charge les modèles (mise en cache)"""
    classifier = DiscoverClassifier()
    pattern_detector = PatternDetector()
    feature_extractor = FeatureExtractor()
    return classifier, pattern_detector, feature_extractor

def main():
    st.markdown('<h1 class="main-header">🔍 Discover Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Analyseur de titres Google Discover - Extraction de patterns haute performance")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Chargement des données")
        
        # Upload du fichier
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=['csv'],
            help="Le fichier doit contenir une colonne avec les titres"
        )
        
        if uploaded_file:
            # Options de configuration
            st.subheader("⚙️ Configuration")
            
            # Prévisualisation
            df_preview = pd.read_csv(uploaded_file, nrows=5)
            
            # Sélection de la colonne
            title_column = st.selectbox(
                "Colonne contenant les titres",
                options=df_preview.columns.tolist(),
                index=0 if 'Title' in df_preview.columns else 0
            )
            
            # Bouton d'analyse
            analyze_button = st.button("🚀 Lancer l'analyse", type="primary")
            
    # Zone principale
    if uploaded_file and analyze_button:
        # Charger les données complètes
        df = pd.read_csv(uploaded_file)
        
        # Vérifier la colonne
        if title_column not in df.columns:
            st.error(f"Colonne '{title_column}' non trouvée!")
            return
            
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Charger les modèles
        status_text.text("Chargement des modèles...")
        classifier, pattern_detector, feature_extractor = load_models()
        progress_bar.progress(20)
        
        # Classification
        status_text.text("Classification des titres...")
        titles = df[title_column].dropna().tolist()
        df_classified = classifier.classify_batch(titles[:1000])  # Limiter pour la démo
        progress_bar.progress(40)
        
        # Extraction des patterns
        status_text.text("Détection des patterns...")
        patterns_by_category = pattern_detector.analyze_patterns_by_category(df_classified)
        progress_bar.progress(60)
        
        # Extraction des features
        status_text.text("Extraction des features linguistiques...")
        df_features = feature_extractor.extract_batch_features(titles[:1000])
        progress_bar.progress(80)
        
        # Génération des insights
        status_text.text("Génération des insights...")
        insights = pattern_detector.generate_pattern_insights(patterns_by_category)
        progress_bar.progress(100)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Affichage des résultats
        display_results(df_classified, patterns_by_category, df_features, insights)
        
    elif not uploaded_file:
        # Page d'accueil
        display_home()

def display_home():
    """Affiche la page d'accueil"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 📊 Classification automatique
        - 12 catégories Google Discover
        - Modèle NLP français
        - Score de confiance
        """)
        
    with col2:
        st.success("""
        ### 🔍 Détection de patterns
        - Structures gagnantes
        - Mots déclencheurs
        - Formules d'accroche
        """)
        
    with col3:
        st.warning("""
        ### 📈 Insights actionnables
        - Templates par catégorie
        - Recommandations
        - Exports multiples
        """)

def display_results(df_classified, patterns_by_category, df_features, insights):
    """Affiche les résultats de l'analyse"""
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'ensemble", 
        "🏷️ Analyse par catégorie",
        "🔍 Patterns détectés", 
        "📈 Features linguistiques",
        "💡 Recommandations"
    ])
    
    with tab1:
        display_overview(df_classified)
        
    with tab2:
        display_category_analysis(df_classified, patterns_by_category)
        
    with tab3:
        display_patterns(patterns_by_category)
        
    with tab4:
        display_features(df_features)
        
    with tab5:
        display_recommendations(insights, df_classified)

def display_overview(df_classified):
    """Affiche la vue d'ensemble"""
    st.header("Vue d'ensemble de l'analyse")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de titres", len(df_classified))
        
    with col2:
        high_conf = len(df_classified[df_classified['confidence'] > 0.7])
        st.metric("Haute confiance", f"{high_conf} ({high_conf/len(df_classified)*100:.1f}%)")
        
    with col3:
        multi_cat = len(df_classified[df_classified['secondary_categories'].apply(len) > 0])
        st.metric("Multi-catégories", f"{multi_cat} ({multi_cat/len(df_classified)*100:.1f}%)")
        
    with col4:
        avg_conf = df_classified['confidence'].mean()
        st.metric("Confiance moyenne", f"{avg_conf:.2%}")
    
    # Distribution des catégories
    st.subheader("Distribution des catégories")
    
    fig = px.pie(
        df_classified, 
        names='main_category_name',
        title="Répartition des titres par catégorie",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top titres par catégorie
    st.subheader("Exemples de titres par catégorie")
    
    for category in df_classified['main_category_name'].value_counts().head(5).index:
        with st.expander(f"{category}"):
            examples = df_classified[df_classified['main_category_name'] == category].head(3)
            for _, row in examples.iterrows():
                st.write(f"- {row['title']} *(confiance: {row['confidence']:.2f})*")

def display_category_analysis(df_classified, patterns_by_category):
    """Affiche l'analyse détaillée par catégorie"""
    st.header("Analyse détaillée par catégorie")
    
    # Sélection de la catégorie
    category = st.selectbox(
        "Sélectionner une catégorie",
        options=sorted(patterns_by_category.keys())
    )
    
    if category in patterns_by_category:
        data = patterns_by_category[category]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Statistiques")
            st.metric("Nombre de titres", data['total_titles'])
            st.metric("Longueur moyenne", f"{data['avg_length']:.0f} caractères")
            st.metric("Plage de longueur", f"{data['length_range'][0]} - {data['length_range'][1]}")
            
        with col2:
            st.subheader("🔤 Mots-clés fréquents")
            words = data['unique_words'][:10]
            st.write(", ".join(words))
            
        # Top patterns
        st.subheader("🎯 Patterns dominants")
        for pattern in data['top_patterns']:
            st.markdown(f"""
            <div class="pattern-box">
                <strong>{pattern['type']}</strong> ({pattern['count']} occurrences)<br>
                Exemples: <em>{pattern['examples'][0][:80]}...</em>
            </div>
            """, unsafe_allow_html=True)

def display_patterns(patterns_by_category):
    """Affiche les patterns détectés"""
    st.header("Patterns détectés dans les titres")
    
    # Agréger tous les patterns
    all_patterns = {}
    for category, data in patterns_by_category.items():
        for pattern_type, count in data['structures'].items():
            if pattern_type not in all_patterns:
                all_patterns[pattern_type] = 0
            all_patterns[pattern_type] += count
            
    # Top patterns globaux
    st.subheader("Top 10 patterns globaux")
    
    top_patterns = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
    
    df_patterns = pd.DataFrame(top_patterns, columns=['Pattern', 'Occurrences'])
    
    fig = px.bar(
        df_patterns, 
        x='Occurrences', 
        y='Pattern',
        orientation='h',
        title="Patterns les plus fréquents"
    )
    st.plotly_chart(fig, use_container_width=True)

def display_features(df_features):
    """Affiche l'analyse des features linguistiques"""
    st.header("Analyse des features linguistiques")
    
    # Sélection des features à afficher
    numeric_cols = df_features.select_dtypes(include=['number']).columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        feature1 = st.selectbox("Feature 1", numeric_cols, index=0)
        
    with col2:
        feature2 = st.selectbox("Feature 2", numeric_cols, index=1)
        
    # Scatter plot
    fig = px.scatter(
        df_features, 
        x=feature1, 
        y=feature2,
        title=f"Relation entre {feature1} et {feature2}",
        opacity=0.6
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution des features
    st.subheader("Distribution des features principales")
    
    key_features = ['length', 'word_count', 'has_numbers', 'power_words_count']
    
    fig_dist = px.box(
        df_features[key_features],
        title="Distribution des features clés"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

def display_recommendations(insights, df_classified):
    """Affiche les recommandations"""
    st.header("💡 Recommandations par catégorie")
    
    for category, recommendations in insights.items():
        with st.expander(f"📌 {category}"):
            for rec in recommendations:
                st.write(f"• {rec}")
                
    # Templates suggérés
    st.subheader("📝 Templates de titres haute performance")
    
    templates = [
        "🔢 [Nombre] [Objet] pour [Bénéfice] en [Temps]",
        "❓ Comment [Action] sans [Obstacle] ?",
        "⚡ Cette [Méthode] [Adjectif] qui [Résultat]",
        "🎯 [Expert] révèle : [Secret] pour [Objectif]",
        "⏰ Avant qu'il soit trop tard : [Action urgente]"
    ]
    
    for template in templates:
        st.code(template)

if __name__ == "__main__":
    main()