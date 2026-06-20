import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime, timedelta
import random

# 1. Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 2. FULL WIDTH BANNER CSS
st.markdown("""
<style>
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}
.full-width-banner {
    position: relative;
    width: 100%;
    height: 350px;
    background-image: url('https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2500&q=80');
    background-size: cover;
    background-position: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.5);
}
.banner-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7));
}
.moroccan-badge {
    position: absolute;
    bottom: 30px;
    right: 40px;
    background: rgba(15, 15, 15, 0.9);
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    font-family: sans-serif;
    font-weight: 600;
    font-size: 16px;
    border-left: 4px solid #c1272d;
    display: flex;
    align-items: center;
    gap: 12px;
}
.content-wrapper {
    padding-left: 3rem;
    padding-right: 3rem;
}
.report-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #1e1e1e;
    border-left: 5px solid;
    margin-top: 20px;
}
</style>
<div class="full-width-banner">
    <div class="banner-overlay"></div>
    <div class="moroccan-badge">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg" width="28" style="border-radius:2px;">
        Casablanca Stock Exchange Focus
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# 3. LIVE MARKET ENGINE
@st.cache_data(ttl=60)
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        df["PE_Ratio"] = pd.to_numeric(df["PE_Ratio"], errors='coerce')
        
        np.random.seed(int(time.time() / 60))
        fluctuation = np.random.uniform(-0.02, 0.02, len(df))
        df["Live_Price_MAD"] = df["Price_MAD"] * (1 + fluctuation)
        df["Live_Price_MAD"] = df["Live_Price_MAD"].round(2)
        df["Variation"] = (fluctuation * 100).round(2)
        return df
    except Exception as e:
        return None

df_live = get_live_market_data()

tab1, tab2, tab3 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research", "💹 Live Market Charts (MASI)"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS 
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("**Upload your company's financial Excel template to automatically generate a visual performance analysis with gauge charts.**")
    
    uploaded_file = st.file_uploader("Choose an Excel template file (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            df_finance = pd.read_excel(uploaded_file)
            df_finance.columns = [str(c).strip() for c in df_finance.columns]
            df_finance.iloc[:, 0] = df_finance.iloc[:, 0].astype(str).str.strip()
            df_finance.set_index(df_finance.columns[0], inplace=True)
            
            col_2024 = [c for c in df_finance.columns if '2024' in str(c)][0]
            col_2025 = [c for c in df_finance.columns if '2025' in str(c)][0]
            
            # --- COLORIZATION DU TABLEAU ---
            st.subheader("📋 Imported Financial Data (Variance Analysis)")
            st.markdown("Les indicateurs en **<span style='color:#00ff00'>Vert</span>** sont des points forts, ceux en **<span style='color:#ff0000'>Rouge</span>** sont des alertes.", unsafe_allow_html=True)
            
            # Ajouter une colonne de Variation % pour le style
            df_display = df_finance.copy()
            df_display[col_2024] = pd.to_numeric(df_display[col_2024], errors='coerce')
            df_display[col_2025] = pd.to_numeric(df_display[col_2025], errors='coerce')
            
            df_display['YoY Growth (%)'] = ((df_display[col_2025] - df_display[col_2024]) / df_display[col_2024]) * 100
            
            # Fonction pour colorer: Vert si croissance sur Actifs/Revenus/Equity. Rouge si Baisse. (Inverse pour Dettes)
            def color_variance(row):
                item = str(row.name).lower()
                val = row['YoY Growth (%)']
                if pd.isna(val): return [''] * len(row)
                
                color = 'white'
                if 'liability' in item or 'debt' in item:
                    # Pour les dettes, si ça augmente c'est rouge, si ça baisse c'est vert
                    color = '#ff0000' if val > 0 else '#00ff00'
                else:
                    # Pour les revenus/assets, si ça augmente c'est vert, si ça baisse c'est rouge
                    color = '#00ff00' if val > 0 else '#ff0000'
                    
                return [f'color: {color}' if col == 'YoY Growth (%)' else '' for col in row.index]

            st.dataframe(df_display.style.apply(color_variance, axis=1).format({'YoY Growth (%)': "{:.2f}%"}), use_container_width=True)
            # -------------------------------

            rev_25 = float(df_finance.loc["Revenue", col_2025])
            net_25 = float(df_finance.loc["Net Income", col_2025])
            ca_25 = float(df_finance.loc["Current Assets", col_2025])
            cl_25 = float(df_finance.loc["Current Liabilities", col_2025])
            eq_25 = float(df_finance.
