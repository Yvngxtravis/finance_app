import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 1. BANNER / HEADER IMAGE
# Utilisation d'une image pro finance/maroc (tu pourras la changer par une image locale si tu veux)
st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80", 
         caption="Z.ELAIDI Financial Analytics Hub | Casablanca Stock Market Automation", use_container_width=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# Création des deux oglets (Tabs)
tab1, tab2 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("Uploadi l-fichier Excel dial l-entreprise باش تخرج ليك l-analyse automatique.")
    
    uploaded_file = st.file_uploader("Choisissez le fichier Excel template", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # FIX: Lecture de l'excel sans mettre la colonne 0 comme index direct pour éviter les erreurs de type
            df_finance = pd.read_excel(uploaded_file)
            
            # Nettoyage des espaces dans les noms de colonnes
            df_finance.columns = [str(c).strip() for c in df_finance.columns]
            df_finance.iloc[:, 0] = df_finance.iloc[:, 0].str.strip()
            
            # Mettre l'item comme index
            df_finance.set_index(df_finance.columns[0], inplace=True)
            
            st.subheader("📋 Données Financières Importées")
            st.dataframe(df_finance)
            
            # FIX: Conversion des colonnes en string/int pour matcher l'index correctement
            col_2024 = [c for c in df_finance.columns if '2024' in str(c)][0]
            col_2025 = [c for c in df_finance.columns if '2025' in str(c)][0]
            
            rev_24, rev_25 = float(df_finance.loc["Revenue", col_2024]), float(df_finance.loc["Revenue", col_2025])
            net_24, net_25 = float(df_finance.loc["Net Income", col_2024]), float(df_finance.loc["Net Income", col_2025])
            ca_24, ca_25 = float(df_finance.loc["Current Assets", col_2024]), float(df_finance.loc["Current Assets", col_2025])
            cl_24, cl_25 = float(df_finance.loc["Current Liabilities", col_2024]), float(df_finance.loc["Current Liabilities", col_2025])
            eq_24, eq_25 = float(df_finance.loc["Total Equity", col_2024]), float(df_finance.loc["Total Equity", col_2025])
            
            # Calcul des Ratios
            current_ratio_24 = ca_24 / cl_24
            current_ratio_25 = ca_25 / cl_25
            net_margin_24 = (net_24 / rev_24) * 100
            net_margin_25 = (net_25 / rev_25) * 100
            roe_24 = (net_24 / eq_24) * 100
            roe_25 = (net_25 / eq_25) * 100
            
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
# TAB 2: EQUITY RESEARCH (LIVE MAROC MARKET DATA)
# ==========================================
with tab2:
    st.header("🏗️ BTP Sector Market Live Dashboard (Casablanca)")
    st.markdown("Comparaison des multiples de valorisation mis à jour en direct.")
    
    try:
        # Lecture de la base BTP
        df_btp = pd.read_csv("btp_market_data.csv")
        
        # Nettoyage des colonnes
        df_btp["Price_MAD"] = pd.to_numeric(df_btp["Price_MAD"])
        df_btp["Market_Cap_Billion"] = pd.to_numeric(df_btp["Market_Cap_Billion"])
        df_btp["PE_Ratio"] = pd.to_numeric(df_btp["PE_Ratio"])
        
        st.subheader("📋 Tableau Comparatif Sectoriel")
        
        # FIX: Changement du style Pink vers un Bleu élégant/sobre pour le max
        st.dataframe(df_btp.style.highlight_max(axis=0, subset=["Market_Cap_Billion", "PE_Ratio"], color="#1f77b4"))
        
        # Graphique Plotly
        st.subheader("📊 Visualisation des Multiples: P/E Ratio")
        fig = px.bar(df_btp, x="Company", y="PE_Ratio", 
                     color="Company", 
                     title="Multiples de Cours sur Bénéfices (P/E Ratio) - BTP Maroc",
                     text_auto=True,
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.error("Le fichier 'btp_market_data.csv' est introuvable.")

# ==========================================
# 4. FOOTER: BY ELAIDI ZAKARIA
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        © 2026 | Automated Financial Analytics Platform | <b>By ELAIDI ZAKARIA</b>
    </div>
    """, 
    unsafe_allow_html=True
)
