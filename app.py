import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta, date

# Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 1. BANNER DYNAMIC AVEC ANIMATION CSS (Fade from left)
st.markdown("""
<style>
@keyframes fadeinleft {
    from { opacity: 0; transform: translateX(-50px); }
    to   { opacity: 1; transform: translateX(0); }
}
.banner-img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    animation: fadeinleft 1.5s ease-out;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
<img class="banner-img" src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1500&q=80" alt="Finance Banner">
""", unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# Création de 3 Tabs d'investissement
tab1, tab2, tab3 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research", "💹 Live Market Charts (MASI)"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS (FIXED)
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("Uploadi l-fichier Excel dial l-entreprise باش تخرج ليك l-analyse automatique.")
    
    uploaded_file = st.file_uploader("Choisissez le fichier Excel template", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # FIX: Lecture plus robuste pour éviter l'erreur .str
            df_finance = pd.read_excel(uploaded_file)
            
            # Conversion forcée en string pour nettoyer les espaces bla machakil
            df_finance.columns = [str(c).strip() for c in df_finance.columns]
            df_finance.iloc[:, 0] = df_finance.iloc[:, 0].astype(str).str.strip()
            
            # Mettre l'item comme index
            df_finance.set_index(df_finance.columns[0], inplace=True)
            
            st.subheader("📋 Données Financières Importées")
            st.dataframe(df_finance)
            
            col_2024 = [c for c in df_finance.columns if '2024' in str(c)][0]
            col_2025 = [c for c in df_finance.columns if '2025' in str(c)][0]
            
            rev_24, rev_25 = float(df_finance.loc["Revenue", col_2024]), float(df_finance.loc["Revenue", col_2025])
            net_24, net_25 = float(df_finance.loc["Net Income", col_2024]), float(df_finance.loc["Net Income", col_2025])
            ca_24, ca_25 = float(df_finance.loc["Current Assets", col_2024]), float(df_finance.loc["Current Assets", col_2025])
            cl_24, cl_25 = float(df_finance.loc["Current Liabilities", col_2024]), float(df_finance.loc["Current Liabilities", col_2025])
            eq_24, eq_25 = float(df_finance.loc["Total Equity", col_2024]), float(df_finance.loc["Total Equity", col_2025])
            
            current_ratio_24 = ca_24 / cl_24
            current_ratio_25 = ca_25 / cl_25
            net_margin_24 = (net_24 / rev_24) * 100
            net_margin_25 = (net_25 / rev_25) * 100
            roe_24 = (net_24 / eq_24) * 100
            roe_25 = (net_25 / eq_25) * 100
            
            st.subheader("📊 Ratios Clés de Performance")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="Current Ratio (2025)", value=f"{current_ratio_25:.2f}", delta=f"{current_ratio_25 - current_ratio_24:.2f} vs 2024")
            with col2:
                st.metric(label="Marge Nette (2025)", value=f"{net_margin_25:.1f}%", delta=f"{net_margin_25 - net_margin_24:.1f}% vs 2024")
            with col3:
                st.metric(label="ROE (2025)", value=f"{roe_25:.1f}%", delta=f"{roe_25 - roe_24:.1f}% vs 2024")
            
            st.subheader("💡 Rapport d'Analyse Automatique")
            if current_ratio_25 >= 1.5:
                liq_status = "Excellent niveau de liquidité. L'entreprise peut couvrir ses dettes à court terme sans problème."
            else:
                liq_status = "⚠️ Risque de liquidité ou niveau juste acceptable. À surveiller."
                
            if net_margin_25 > net_margin_24:
                prof_status = f"Amélioration de la rentabilité opérationnelle ({net_margin_25:.1f}%)."
            else:
                prof_status = "Baisse de la rentabilité opérationnelle."
                
            st.info(f"**Liquidité:** {liq_status}\n\n**Rentabilité:** {prof_status}")
            
        except Exception as e:
            st.error(f"Erreur de lecture du fichier. Veuillez vérifier le format. Détails: {e}")

# ==========================================
# TAB 2: EQUITY RESEARCH (REAL DATA)
# ==========================================
with tab2:
    st.header("🏗️ BTP Sector Market Dashboard (Casablanca)")
    try:
        df_btp = pd.read_csv("btp_market_data.csv")
        df_btp["Price_MAD"] = pd.to_numeric(df_btp["Price_MAD"])
        df_btp["PE_Ratio"] = pd.to_numeric(df_btp["PE_Ratio"])
        
        st.subheader("📋 Tableau Comparatif Sectoriel")
        st.dataframe(df_btp.style.highlight_max(axis=0, subset=["Market_Cap_Billion", "PE_Ratio"], color="#1f77b4"))
        
        st.subheader("📊 Visualisation: P/E Ratio vs Market Cap")
        fig = px.bar(df_btp, x="Company", y="PE_Ratio", color="Company", title="P/E Ratio par Entreprise (BTP Maroc)", text_auto=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur de chargement des données BTP: {e}")

# ==========================================
# TAB 3: LIVE MARKET CHARTS (Candlesticks)
# ==========================================
with tab3:
    st.header("💹 Simulation Bourse de Casablanca (MASI Live Trend)")
    st.markdown("Analyse technique et comportement des actions du secteur.")
    
    try:
        selected_company = st.selectbox("Sélectionnez l'entreprise à analyser:", df_btp["Company"].tolist())
        
        # Génération de données boursières réalistes pour l'affichage LinkedIn
        base_price = df_btp[df_btp["Company"] == selected_company]["Price_MAD"].values[0]
        
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        np.random.seed(42 + len(selected_company)) # Seed basé sur le nom pour garder le même chart
        
        # Random walk volatility
        volatility = base_price * 0.02
        price_changes = np.random.normal(0, volatility, size=30)
        close_prices = base_price + np.cumsum(price_changes)
        open_prices = close_prices - np.random.normal(0, volatility/2, size=30)
        high_prices = np.maximum(open_prices, close_prices) + np.abs(np.random.normal(0, volatility/3, size=30))
        low_prices = np.minimum(open_prices, close_prices) - np.abs(np.random.normal(0, volatility/3, size=30))
        
        fig_candle = go.Figure(data=[go.Candlestick(x=dates, open=open_prices, high=high_prices, low=low_prices, close=close_prices)])
        fig_candle.update_layout(title=f"Evolution du cours - {selected_company} (30 Derniers Jours)",
                                 yaxis_title="Prix (MAD)",
                                 template="plotly_dark",
                                 xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig_candle, use_container_width=True)
    except Exception as e:
        st.warning("Veuillez vérifier les données pour afficher le graphique.")

# ==========================================
# FOOTER: BY ELAIDI ZAKARIA
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #a0a0a0; font-size: 15px; letter-spacing: 1px;'>
        © 2026 | Automated Financial Analytics Platform | <b>By ELAIDI ZAKARIA</b>
    </div>
    """, 
    unsafe_allow_html=True
)
