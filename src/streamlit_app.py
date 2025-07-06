"""
Dashboard Streamlit pour l'analyse des titres Google Discover
Version optimisée pour éviter les timeouts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import sys
sys.path.append('..')

# Import des modules locaux
from src.classifier import DiscoverClassifier
from src.pattern_detector import PatternDetector
from src.feature_extractor import FeatureExtractor

# Configuration de la page
st.set_page_config(
    page_title="Analyseur Google Discover",
    page_icon="📊",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Charge les modèles en cache"""
    classifier = DiscoverClassifier()
    pattern_detector = PatternDetector()
    feature_extractor = FeatureExtractor()
    return classifier, pattern_detector, feature_extractor

def main():
    st.markdown("<h1 class='main-header'>📋 Analyseur de Titres Google Discover</h1>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Upload du fichier
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=['csv'],
            help="Le fichier doit contenir une colonne avec les titres"
        )
        
        if uploaded_file:
            # Détection des colonnes
            df_preview = pd.read_csv(uploaded_file, nrows=5)
            columns = df_preview.columns.tolist()
            
            title_column = st.selectbox(
                "Colonne contenant les titres",
                columns,
                index=0 if 'Title' in columns else 0
            )
            
            # Options d'analyse
            st.subheader("Options d'analyse")
            analyze_patterns = st.checkbox("Analyser les patterns", value=True)
            extract_features = st.checkbox("Extraire les features", value=True)
            
    # Contenu principal
    if uploaded_file is not None:
        # Charger les données
        df = pd.read_csv(uploaded_file)
        st.info(f"📊 {len(df)} titres chargés")
        
        # Bouton d'analyse
        if st.button("🚀 Lancer l'analyse", type="primary"):
            with st.spinner("Analyse en cours..."):
                # Charger les modèles
                classifier, pattern_detector, feature_extractor = load_models()
                
                # Classification
                titles = df[title_column].tolist()
                df_classified = classifier.classify_batch(titles)
                
                # Analyse de distribution
                distribution = classifier.analyze_distribution(df_classified)
                
                # Affichage des résultats
                st.success("✅ Analyse terminée!")
                
                # Métriques principales
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total de titres", distribution['total_titles'])
                with col2:
                    st.metric("Haute confiance", distribution['high_confidence_titles'])
                with col3:
                    st.metric("Multi-catégories", distribution['multi_category_titles'])
                with col4:
                    st.metric("Catégories", len(distribution['distribution']))
                
                # Graphiques
                st.subheader("📊 Distribution par catégorie")
                
                # Pie chart
                fig_pie = px.pie(
                    values=list(distribution['distribution'].values()),
                    names=list(distribution['distribution'].keys()),
                    title="Répartition des titres par catégorie"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Bar chart
                fig_bar = px.bar(
                    x=list(distribution['distribution'].keys()),
                    y=list(distribution['distribution'].values()),
                    title="Nombre de titres par catégorie",
                    labels={'x': 'Catégorie', 'y': 'Nombre de titres'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Patterns par catégorie
                if analyze_patterns:
                    st.subheader("🔍 Analyse des patterns")
                    
                    # Sélection de la catégorie
                    categories = df_classified['main_category_name'].unique()
                    selected_category = st.selectbox("Sélectionner une catégorie", categories)
                    
                    # Filtrer les titres de la catégorie
                    cat_titles = df_classified[
                        df_classified['main_category_name'] == selected_category
                    ]['title'].tolist()
                    
                    # Détecter les patterns
                    structures = pattern_detector.detect_structures(cat_titles[:100])  # Limiter pour performance
                    
                    # Afficher les patterns trouvés
                    if structures:
                        st.write(f"**Patterns trouvés pour {selected_category}:**")
                        
                        # Top patterns
                        pattern_counts = {k: len(v) for k, v in structures.items()}
                        top_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                        
                        for pattern_name, count in top_patterns:
                            with st.expander(f"{pattern_name} ({count} occurrences)"):
                                examples = structures[pattern_name][:3]
                                for ex in examples:
                                    st.write(f"- {ex}")
                
                # Export des résultats
                st.subheader("💾 Export des résultats")
                
                # Préparer les données pour export
                export_df = pd.concat([df, df_classified], axis=1)
                
                # Bouton de téléchargement
                csv = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv,
                    file_name="resultats_analyse_discover.csv",
                    mime="text/csv"
                )
                
    else:
        # Instructions
        st.markdown("""
        ### 🚀 Comment utiliser cet outil ?
        
        1. **Uploadez votre fichier CSV** contenant les titres dans la sidebar
        2. **Sélectionnez la colonne** contenant les titres
        3. **Configurez les options** d'analyse
        4. **Cliquez sur "Lancer l'analyse"**
        
        ### 📋 Format attendu
        
        Votre fichier CSV doit contenir au minimum une colonne avec les titres d'articles.
        
        ### 🎯 Catégories analysées
        
        L'outil classe automatiquement les titres dans 12 catégories :
        
        - 🏥 Santé Naturelle
        - 💪 Sport & Fitness
        - 🌸 Beauté Anti-âge
        - 🏛️ Société & Tendances
        - 🗺️ Voyages & Découvertes
        - 🌿 Lifestyle & Bien-être
        - 🎨 Culture & Patrimoine
        - 🧠 Psychologie & Mental
        - 👴 Senior & Vieillissement
        - 🚗 Automobile & Mobilité
        - 💰 Finance & Investissement
        - 🍽️ Recettes & Cuisine
        """)

if __name__ == "__main__":
    main()