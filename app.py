import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Financial Analytics Hub", layout="wide", page_icon="📊")

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# Création des deux onglets (Tabs)
tab1, tab2 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("Uploadi l-fichier Excel dial l-entreprise باش تخرج ليك l-analyse automatique.")
    
    # Upload du fichier Excel
    uploaded_file = st.file_uploader("Choisissez le fichier Excel template", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # Lecture du fichier
            df_finance = pd.read_excel(uploaded_file, index_col=0)
            st.subheader("📋 Données Financières Importées")
            st.dataframe(df_finance)
            
            # Extraction delle values pour les calculs
            rev_24, rev_25 = df_finance.loc["Revenue", 2024], df_finance.loc["Revenue", 2025]
            net_24, net_25 = df_finance.loc["Net Income", 2024], df_finance.loc["Net Income", 2025]
            ca_24, ca_25 = df_finance.loc["Current Assets", 2024], df_finance.loc["Current Assets", 2025]
            cl_24, cl_25 = df_finance.loc["Current Liabilities", 2024], df_finance.loc["Current Liabilities", 2025]
            eq_24, eq_25 = df_finance.loc["Total Equity", 2024], df_finance.loc["Total Equity", 2025]
            
            # Calcul des Ratios
            current_ratio_24 = ca_24 / cl_24
            current_ratio_25 = ca_25 / cl_25
            
            net_margin_24 = (net_24 / rev_24) * 100
            net_margin_25 = (net_25 / rev_25) * 100
            
            roe_24 = (net_24 / eq_24) * 100
            roe_25 = (net_25 / eq_25) * 100
            
            # Affichage des KPIs dans des colonnes
            st.subheader("📊 Ratios Clés de Performance")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="Current Ratio (2025)", value=f"{current_ratio_25:.2f}", 
                          delta=f"{current_ratio_25 - current_ratio_24:.2f} vs 2024")
            with col2:
                st.metric(label="Marge Nette (2025)", value=f"{net_margin_25:.1f}%", 
                          delta=f"{net_margin_25 - net_margin_24:.1f}% vs 2024")
            with col3:
                st.metric(label="ROE (2025)", value=f"{roe_25:.1f}%", 
                          delta=f"{roe_25 - roe_24:.1f}% vs 2024")
            
            # Interpretation Automatique (Storytelling)
            st.subheader("💡 Rapport d'Analyse Automatique")
            if current_ratio_25 >= 1.5:
                liq_status = "Excellent niveau de liquidité. L'entreprise peut couvrir ses dettes à court terme sans problème."
            elif current_ratio_25 >= 1.0:
                liq_status = "Niveau de liquidité acceptable, mais à surveiller de près."
            else:
                liq_status = "⚠️ Risque de liquidité! Les actifs circulants sont insuffisants pour couvrir le passif court terme."
                
            if net_margin_25 > net_margin_24:
                prof_status = f"Amélioration de la rentabilité. La marge nette est passée de {net_margin_24:.1f}% à {net_margin_25:.1f}%."
            else:
                prof_status = "Baisse de la rentabilité opérationnelle ou augmentation des charges."
                
            st.info(f"**Liquidité:** {liq_status}\n\n**Rentabilité:** {prof_status}")
            
        except Exception as e:
            st.error(f"Erreur de lecture du fichier. Vérifiez le format du template. Détails: {e}")
    else:
        st.warning("En attente de l'upload du fichier Excel template pour générer l'analyse.")

# ==========================================
# TAB 2: EQUITY RESEARCH (BTP SECTOR)
# ==========================================
with tab2:
    st.header("🏗️ BTP Sector Market Dashboard (Casablanca)")
    st.markdown("Comparaison des multiples de valorisation des grandes entreprises du secteur BTP.")
    
    try:
        # Lecture de la base BTP
        df_btp = pd.read_csv("btp_market_data.csv")
        
        # Sidebar/Filtres pour le secteur BTP
        st.subheader("🔍 Filtres & Sélection")
        companies_selected = st.multiselect("Sélectionnez les entreprises à comparer:", 
                                            options=df_btp["Company"].unique(), 
                                            default=df_btp["Company"].unique())
        
        df_filtered = df_btp[df_btp["Company"].isin(companies_selected)]
        
        # Table comparative
        st.dataframe(df_filtered.style.highlight_max(axis=0, subset=["Market_Cap_Billion", "PE_Ratio"], color="#ffe6e6"))
        
        # Graphique Plotly dynamique
        st.subheader("📊 Visualisation des Multiples: P/E Ratio vs Market Cap")
        fig = px.bar(df_filtered, x="Company", y="PE_Ratio", 
                     color="Company", 
                     title="Multiples de Cours sur Bénéfices (P/E Ratio)",
                     text_auto=True,
                     labels={"PE_Ratio": "P/E Ratio", "Company": "Entreprise"})
        st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.error("Le fichier 'btp_market_data.csv' est introuvable. Assurez-vous qu'il est dans le même dossier.")