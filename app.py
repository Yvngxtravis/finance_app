import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta, date

# 1. Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 2. Fix Padding & Banner 100% Width
st.markdown("""
<style>
/* N-7iydo l'marge l'fou9aniya dial Streamlit */
.block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
}
.banner-container {
    position: relative;
    width: 100%;
    height: 300px;
    margin-bottom: 30px;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0,0,0,0.5);
}
.banner-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.85);
}
.moroccan-badge {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: rgba(20, 20, 20, 0.9);
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-family: sans-serif;
    font-weight: 600;
    font-size: 16px;
    border-left: 4px solid #c1272d;
    display: flex;
    align-items: center;
    gap: 12px;
}
</style>
<div class="banner-container">
    <img class="banner-img" src="https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2000&q=80" alt="Finance Banner">
    <div class="moroccan-badge">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg" width="28" style="border-radius:2px;">
        Casablanca Stock Exchange Focus
    </div>
</div>
""", unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# 3. Création des 3 Tabs
tab1, tab2, tab3 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research", "💹 Live Market Charts (MASI)"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS 
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("**Upload your company's financial Excel template to automatically generate a visual performance analysis with gauge charts.**")
    
    uploaded_file = st.file_uploader("Choose an Excel template file", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            df_finance = pd.read_excel(uploaded_file)
            df_finance.columns = [str(c).strip() for c in df_finance.columns]
            df_finance.iloc[:, 0] = df_finance.iloc[:, 0].astype(str).str.strip()
            df_finance.set_index(df_finance.columns[0], inplace=True)
            
            st.subheader("📋 Imported Financial Data")
            st.dataframe(df_finance)
            
            col_2024 = [c for c in df_finance.columns if '2024' in str(c)][0]
