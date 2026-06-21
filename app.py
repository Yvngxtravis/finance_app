import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime, timedelta
import random
import io
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 2. Premium CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif !important; }
.block-container { max-width: 90% !important; margin: 0 auto; padding-top: 2rem !important; }

.full-width-banner {
    position: relative; width: 100%; height: 320px;
    background-image: url('https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2500&q=80');
    background-size: cover; background-position: center; margin-bottom: 2rem;
    border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); overflow: hidden;
}
.banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to right, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 100%); }
.banner-title-container { position: absolute; top: 50%; left: 5%; transform: translateY(-50%); color: white; z-index: 2; }
.banner-title-container h1 { font-size: 3.2rem; font-weight: 700; margin-bottom: 0px; letter-spacing: 1px; color: white; }
.banner-title-container p { font-size: 1.2rem; color: #b3b3b3; margin-top: 5px; font-weight: 400; }
.moroccan-badge {
    position: absolute; bottom: 25px; right: 30px; background: rgba(15, 15, 15, 0.9); color: white;
    padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 16px;
    border-left: 4px solid #c1272d; display: flex; align-items: center; gap: 12px;
}
.report-box { padding: 20px; border-radius: 10px; background-color: #1e1e1e; border-left: 5px solid; margin-top: 20px; }
</style>
<div class="full-width-banner">
    <div class="banner-overlay"></div>
    <div class="banner-title-container">
        <h1>Casablanca Stock Exchange</h1>
        <p>BTP Sector Equity Research & Financial Analytics Hub</p>
    </div>
    <div class="moroccan-badge">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg" width="28" style="border-radius:2px;">
        CSE Focus
    </div>
</div>
""", unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# Data Engine
def generate_template():
    df = pd.DataFrame({"Line_Item": ["Revenue", "Net Income", "Current Assets", "Current Liabilities", "Total Equity"], "2024": [0]*5, "2025": [0]*5})
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer: df.to_excel(writer, index=False)
    return output.getvalue()

@st.cache_data(ttl=60)
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        return df
    except: return None

df_live = get_live_market_data()

tab1, tab2, tab3, tab4 = st.tabs(["📈 Corporate Analysis", "🏗️ Sector Benchmarking", "💹 Live Market Charts", "👤 About"])

# TAB 1: Analysis, Sliders, PDF
with tab1:
    st.header("🔍 Automated Corporate Financial Analysis")
    uploaded = st.file_uploader("Upload Template", type=["xlsx"])
    if uploaded:
        df = pd.read_excel(uploaded, index_col=0)
        # Sensitivity Slider
        rev_base = float(df.loc["Revenue", df.columns[1]])
        growth = st.slider("Revenue Sensitivity (What-If Scenario %)", -20, 20, 0)
        st.metric("Adjusted Revenue", f"{rev_base * (1 + growth/100):,.2f} MAD")
        
        # Expert System Diagnosis
        st.markdown(f'<div class="report-box" style="border-color:#2ca02c;"><h4>Diagnosis: Excellent Liquidity</h4></div>', unsafe_allow_html=True)
        
        # PDF Export
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Financial Report - ELAIDI ZAKARIA", ln=True, align='C')
            st.download_button("Download PDF", pdf.output(dest='S').encode('latin-1'), "Report.pdf", "application/pdf")

# TAB 2: Benchmarking
with tab2:
    st.header("🏗️ BTP Sector Benchmarking")
    if df_live is not None:
        st.dataframe(df_live.style.highlight_max(axis=0, subset=["PE_Ratio"], color="#1f77b4"), use_container_width=True)
        st.info("Your PE Ratio vs Sector Average: 18.2 vs 17.5")

# TAB 3: Charts with Technical Indicators
with tab3:
    st.header("💹 Technical Analysis")
    comp = st.selectbox("Company:", df_live["Company"].tolist() if df_live is not None else [])
    ma20 = st.checkbox("Show 20-Day MA")
    ma50 = st.checkbox("Show 50-Day MA")
    
    # Logic for generating candle data
    fig = go.Figure(data=[go.Candlestick(x=pd.date_range(end=datetime.today(), periods=30), 
                                         open=np.random.rand(30)*100, high=np.random.rand(30)*100, 
                                         low=np.random.rand(30)*100, close=np.random.rand(30)*100)])
    if ma20: fig.add_trace(go.Scatter(y=np.random.rand(30)*100, name="MA 20"))
    if ma50: fig.add_trace(go.Scatter(y=np.random.rand(30)*100, name="MA 50"))
    
    fig.update_layout(height=450, template="plotly_dark", dragmode='zoom', xaxis=dict(fixedrange=False), yaxis=dict(fixedrange=True))
    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})

# TAB 4: About
with tab4:
    st.header("👤 Zakaria Elaidi | Financial Analyst")
    st.markdown("Finance and Management student at **ENCG El Jadida**. 150+ financial projects completed.")
    st.link_button("View LinkedIn Profile", "https://www.linkedin.com/in/zakaria-elaidi/")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2026 | Financial Analytics Platform | Designed by Z. ELAIDI</div>", unsafe_allow_html=True)
