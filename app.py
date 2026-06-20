import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta, date

# Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 1. BANNER DYNAMIC VRAIMENT FULL WIDTH AVEC DRAPEAU MAROCAIN
st.markdown("""
<style>
@keyframes fadeinleft {
    from { opacity: 0; transform: translateX(-50px); }
    to   { opacity: 1; transform: translateX(0); }
}
.full-width-banner {
    position: relative;
    width: 100vw;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    height: 320px;
    margin-top: -60px; /* Bach t-tle3 l'fou9 */
    margin-bottom: 30px;
    overflow: hidden;
    animation: fadeinleft 1.2s ease-out;
}
.banner-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.85); /* Bach l'katba tban mzyan */
}
.moroccan-badge {
    position: absolute;
    bottom: 30px;
    right: 40px;
    background: rgba(15, 15, 15, 0.85);
    color: white;
    padding: 12px 24px;
    border-radius: 30px;
    font-family: sans-serif;
    font-weight: 600;
    font-size: 16px;
    border: 1px solid #c1272d;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
}
</style>
<div class="full-width-banner">
    <img class="banner-img" src="https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2500&q=80" alt="Finance Banner">
    <div class="moroccan-badge">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg" width="28" style="border-radius:2px;">
        Casablanca Stock Exchange Focus
    </div>
</div>
""", unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# Création des 3 Tabs
tab1, tab2, tab3 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research", "💹 Live Market Charts (MASI)"])

# ==========================================
# TAB 1: AUTOMATED FINANCIAL ANALYSIS 
# ==========================================
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    st.markdown("**Upload your company's financial Excel template to automatically generate a visual performance analysis with gauge charts.**")
    
    uploaded_file = st.file_uploader("Choose an Excel template file", type=["xlsx"])
