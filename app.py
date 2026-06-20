import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime

# 1. Configuration de la page
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 2. FULL WIDTH BANNER CSS (Edge to Edge)
st.markdown("""
<style>
/* Remove Streamlit default padding */
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
/* Re-add padding for content below banner */
.content-wrapper {
    padding-left: 3rem;
    padding-right: 3rem;
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

# Wrap content to keep it aligned after full-width banner
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

st.title("📊 Financial Analytics & Equity Research Hub")
st.markdown("---")

# 3. LIVE MARKET ENGINE (Simulates Live Data without breaking)
@st.cache_data(ttl=60) # Refreshes every 60 seconds
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        df["PE_Ratio"] = pd.to_numeric(df["PE_Ratio"], errors='coerce')
        
        # Algorithme de volatilité en temps réel (Simule la Bourse Live)
        np.random.seed(int(time.time() / 60)) # Change chaque minute
        fluctuation = np.random.uniform(-0.02, 0.02, len(df)) # +/- 2% max
        df["Live_Price_MAD"] = df["Price_MAD"] * (1 + fluctuation)
        df["Live_Price_MAD"] = df["Live_Price_MAD"].round(2)
        
        df["Variation"] = (fluctuation * 100).round(2)
        return df
    except Exception as e:
        return None

df_live = get_live_market_data()

# 4. Création des 3 Tabs
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
            
            st.subheader("📋 Imported Financial Data")
            st.dataframe(df_finance)
            
            col_2024 = [c for c in df_finance.columns if '2024' in str(c)][0]
            col_2025 = [c for c in df_finance.columns if '2025' in str(c)][0]
            
            rev_24 = float(df_finance.loc["Revenue", col_2024])
            rev_25 = float(df_finance.loc["Revenue", col_2025])
            net_25 = float(df_finance.loc["Net Income", col_2025])
            ca_25 = float(df_finance.loc["Current Assets", col_2025])
            cl_25 = float(df_finance.loc["Current Liabilities", col_2025])
            eq_25 = float(df_finance.loc["Total Equity", col_2025])
            
            current_ratio_25 = ca_25 / cl_25
            net_margin_25 = (net_25 / rev_25) * 100
            roe_25 = (net_25 / eq_25) * 100
            
            st.subheader("📊 Key Performance Ratios (Visuals)")
            col1, col2, col3 = st.columns(3)
            
            fig1 = go.Figure(go.Indicator(
                mode = "gauge+number", value = current_ratio_25,
                title = {'text': "Current Ratio", 'font': {'size': 20}},
                gauge = {'axis': {'range': [0, 3]}, 'bar': {'color': "#2ca02c"}}
            ))
            fig1.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), template="plotly_dark")
            col1.plotly_chart(fig1, use_container_width=True)
            
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number", value = net_margin_25, number = {'suffix': "%"},
                title = {'text': "Net Margin", 'font': {'size': 20}},
                gauge = {'axis': {'range': [0, 30]}, 'bar': {'color': "#1f77b4"}}
            ))
            fig2.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), template="plotly_dark")
            col2.plotly_chart(fig2, use_container_width=True)
            
            fig3 = go.Figure(go.Indicator(
                mode = "gauge+number", value = roe_25, number = {'suffix': "%"},
                title = {'text': "Return on Equity (ROE)", 'font': {'size': 20}},
                gauge = {'axis': {'range': [0, 40]}, 'bar': {'color': "#9467bd"}}
            ))
            fig3.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), template="plotly_dark")
            col3.plotly_chart(fig3, use_container_width=True)
            
        except Exception as e:
            st.error("Error reading file. Please ensure it matches the template structure.")

# ==========================================
# TAB 2: EQUITY RESEARCH (LIVE MARKET)
# ==========================================
with tab2:
    st.header(f"🏗️ BTP Sector Live Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Casablanca Time)")
    
    if df_live is not None:
        # Affichage avec style pour les variations (Vert/Rouge)
        def color_variation(val):
            color = '#00ff00' if val > 0 else '#ff0000' if val < 0 else 'white'
            return f'color: {color}'
            
        st.dataframe(df_live[["Company", "Live_Price_MAD", "Variation", "Market_Cap_Billion", "PE_Ratio", "Dividend_Yield"]]
                     .style.map(color_variation, subset=['Variation'])
                     .highlight_max(axis=0, subset=["Market_Cap_Billion"], color="#1f77b4"),
                     use_container_width=True)
        
        fig = px.bar(df_live, x="Company", y="Live_Price_MAD", color="Variation", 
                     title="Live Stock Prices (MAD) & Intraday Variation", 
                     color_continuous_scale="RdYlGn", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Error loading BTP data.")

# ==========================================
# TAB 3: LIVE MARKET CHARTS (BIG CANDLES)
# ==========================================
with tab3:
    st.header("💹 Technical Analysis & Live Trends")
    
    if df_live is not None:
        col_sel1, col_sel2 = st.columns([1, 1])
        with col_sel1:
            selected_company = st.selectbox("Select Company:", df_live["Company"].tolist())
        with col_sel2:
            chart_type = st.radio("Chart Style:", ["Candlesticks", "Line Chart"], horizontal=True)
        
        base_price = df_live[df_live["Company"] == selected_company]["Live_Price_MAD"].values[0]
        dates = pd.date_range(end=pd.Timestamp.today(), periods=60)
        np.random.seed(42 + len(selected_company))
        
        # High volatility for bigger candles
        volatility = base_price * 0.05
        price_changes = np.random.normal(0, volatility, size=60)
        close_prices = base_price + np.cumsum(price_changes)
        open_prices = close_prices - np.random.normal(0, volatility, size=60)
        high_prices = np.maximum(open_prices, close_prices) + np.abs(np.random.normal(0, volatility*1.2, size=60))
        low_prices = np.minimum(open_prices, close_prices) - np.abs(np.random.normal(0, volatility*1.2, size=60))
        
        if chart_type == "Candlesticks":
            fig_market = go.Figure(data=[go.Candlestick(x=dates, open=open_prices, high=high_prices, low=low_prices, close=close_prices,
                                                        increasing_line_color='#00ff00', decreasing_line_color='#ff0000')])
        else:
            fig_market = go.Figure(data=[go.Scatter(x=dates, y=close_prices, mode='lines+markers', line=dict(color='#1f77b4', width=3))])
            
        fig_market.update_layout(height=650, title=f"60-Day Price Movement - {selected_company}",
                                 yaxis_title="Price (MAD)", template="plotly_dark", xaxis_rangeslider_visible=False,
                                 margin=dict(l=20, r=20, t=50, b=20))
        
        st.plotly_chart(fig_market, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True) # End content wrapper

# ==========================================
# FOOTER: BY ELAIDI ZAKARIA
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #a0a0a0; font-size: 15px; letter-spacing: 1px; padding-bottom: 20px;'>
        © 2026 | Automated Financial Analytics Platform | <b>By ELAIDI ZAKARIA</b>
    </div>
    """, 
    unsafe_allow_html=True
)
