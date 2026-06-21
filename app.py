import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime, timedelta
import random
import io
import base64
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics Hub", layout="wide", page_icon="📊")

# 2. Premium CSS & Full Width Banner & Animated Button
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 95% !important; 
    margin: 0 auto;
}

.full-width-banner {
    position: relative; width: 100%; height: 320px;
    background-image: url('https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2500&q=80');
    background-size: cover; background-position: center; margin-bottom: 2rem;
    border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); overflow: hidden;
}

.banner-overlay {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(to right, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 100%);
}

.banner-title-container {
    position: absolute; top: 50%; left: 5%; transform: translateY(-50%); color: white; z-index: 2;
}

.banner-title-container h1 { font-size: 3.2rem; font-weight: 700; margin-bottom: 0px; letter-spacing: 1px; color: white; }
.banner-title-container p { font-size: 1.2rem; color: #b3b3b3; margin-top: 5px; font-weight: 400; }

.moroccan-badge {
    position: absolute; bottom: 25px; right: 30px; background: rgba(15, 15, 15, 0.9); color: white;
    padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 16px;
    border-left: 4px solid #c1272d; display: flex; align-items: center; gap: 12px;
}

.report-box { padding: 20px; border-radius: 10px; background-color: #1e1e1e; border-left: 5px solid; margin-top: 20px; }

/* ANIMATED RED DOWNLOAD BUTTON */
.btn-animated-red {
    background: linear-gradient(45deg, #c1272d, #ff3b3b);
    color: white !important;
    padding: 15px 25px;
    text-align: center;
    text-decoration: none;
    display: block;
    font-size: 18px;
    font-weight: 700;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(193, 39, 45, 0.4);
    transition: all 0.3s ease;
    animation: pulse 2s infinite;
    margin-top: 20px;
}

.btn-animated-red:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(193, 39, 45, 0.7);
    color: white !important;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(193, 39, 45, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(193, 39, 45, 0); }
    100% { box-shadow: 0 0 0 0 rgba(193, 39, 45, 0); }
}

.metric-card { background-color: #1e1e1e; padding: 15px; border-radius: 8px; border-top: 3px solid #1f77b4; margin-bottom: 15px; }
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

# ==========================================
# DATA ENGINE & HELPERS
# ==========================================
def generate_template():
    df_template = pd.DataFrame({
        "Line_Item": ["Revenue", "Net Income", "Current Assets", "Current Liabilities", "Inventory", "Total Assets", "Total Equity", "Total Debt"],
        "2024": [0, 0, 0, 0, 0, 0, 0, 0],
        "2025": [0, 0, 0, 0, 0, 0, 0, 0]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_template.to_excel(writer, index=False)
    return output.getvalue()

@st.cache_data(ttl=60)
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        df["PE_Ratio"] = pd.to_numeric(df["PE_Ratio"], errors='coerce')
        np.random.seed(int(time.time() / 60))
        fluctuation = np.random.uniform(-0.02, 0.02, len(df))
        df["Live_Price_MAD"] = (df["Price_MAD"] * (1 + fluctuation)).round(2)
        df["Variation"] = (fluctuation * 100).round(2)
        return df
    except Exception as e:
        return None

df_live = get_live_market_data()

# --- PDF GENERATOR LOGIC ---
def create_pdf(company_ratios, expert_diagnosis, sector_avg_pe, df_display):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "Financial & Equity Research Report", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, f"Generated automatically on: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)
    
    # Corporate Analysis
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "1. Corporate Financial Analysis (Tab 1)", ln=True)
    pdf.set_font("Arial", '', 12)
    for key, value in company_ratios.items():
        pdf.cell(0, 8, f"- {key}: {value}", ln=True)
    pdf.ln(5)
    
    # Expert Diagnosis
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Expert Diagnosis Notes:", ln=True)
    pdf.set_font("Arial", '', 11)
    for note in expert_diagnosis:
        pdf.multi_cell(0, 8, txt=f"* {note}")
    pdf.ln(10)
    
    # Benchmarking
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "2. BTP Sector Benchmarking (Tab 2)", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, txt=f"The company's performance was compared against the Casablanca Stock Exchange BTP sector averages. The average sector PE Ratio is currently {sector_avg_pe:.2f}.")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Report built via Z. ELAIDI Analytics Platform", align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# MAIN TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["📈 Corporate Financial Analysis", "🏗️ BTP Sector Equity Research", "💹 Live Market Charts", "👤 About the Creator"])

# ==========================================
# TAB 1: SPLIT SCREEN LAYOUT
# ==========================================
with tab1:
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.header("🔍 Automated Corporate Financial Analysis")
        st.markdown("**Upload your company's financial Excel template to unlock the dual-pane analysis dashboard.**")
    with col_header2:
        st.download_button(label="📥 Download Required Template", data=generate_template(), file_name="Financial_Template_Standard.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    
    uploaded_file = st.file_uploader("Choose your completed Excel file (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # Data Processing
            df_finance = pd.read_excel(uploaded_file)
            df_finance.columns = [str(c).strip() for c in df_finance.columns]
            df_finance.iloc[:, 0] = df_finance.iloc[:, 0].astype(str).str.strip()
            df_finance.set_index(df_finance.columns[0], inplace=True)
            
            col_2024, col_2025 = [c for c in df_finance.columns if '2024' in str(c)][0], [c for c in df_finance.columns if '2025' in str(c)][0]
            
            # --- START DUAL COLUMN LAYOUT ---
            left_col, right_col = st.columns([1.3, 1], gap="large")
            
            # ==============================
            # LEFT COLUMN (Your original UI)
            # ==============================
            with left_col:
                st.subheader("📋 Imported Variance Analysis")
                df_display = df_finance.copy()
                df_display[col_2024] = pd.to_numeric(df_display[col_2024], errors='coerce')
                df_display[col_2025] = pd.to_numeric(df_display[col_2025], errors='coerce')
                df_display['YoY Growth (%)'] = ((df_display[col_2025] - df_display[col_2024]) / df_display[col_2024]) * 100
                
                def color_variance(row):
                    item, val = str(row.name).lower(), row['YoY Growth (%)']
                    if pd.isna(val): return [''] * len(row)
                    color = '#ff0000' if ('liability' in item or 'debt' in item) and val > 0 else '#00ff00' if val > 0 else '#ff0000'
                    return [f'color: {color}' if col == 'YoY Growth (%)' else '' for col in row.index]

                st.dataframe(df_display.style.apply(color_variance, axis=1).format({'YoY Growth (%)': "{:.2f}%"}), use_container_width=True)

                rev_25 = float(df_finance.loc["Revenue", col_2025])
                net_25 = float(df_finance.loc["Net Income", col_2025])
                ca_25 = float(df_finance.loc["Current Assets", col_2025])
                cl_25 = float(df_finance.loc["Current Liabilities", col_2025])
                eq_25 = float(df_finance.loc["Total Equity", col_2025])
                
                current_ratio_25 = ca_25 / cl_25
                net_margin_25 = (net_25 / rev_25) * 100
                roe_25 = (net_25 / eq_25) * 100
                
                st.subheader("📊 Key Performance Ratios")
                c1, c2, c3 = st.columns(3)
                
                fig1 = go.Figure(go.Indicator(mode="gauge+number", value=current_ratio_25, title={'text': "Current Ratio", 'font': {'size': 14}}, gauge={'axis': {'range': [0, 3]}, 'bar': {'color': "#2ca02c"}}))
                fig1.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), template="plotly_dark")
                c1.plotly_chart(fig1, use_container_width=True)
                
                fig2 = go.Figure(go.Indicator(mode="gauge+number", value=net_margin_25, number={'suffix': "%"}, title={'text': "Net Margin", 'font': {'size': 14}}, gauge={'axis': {'range': [0, 30]}, 'bar': {'color': "#1f77b4"}}))
                fig2.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), template="plotly_dark")
                c2.plotly_chart(fig2, use_container_width=True)
                
                fig3 = go.Figure(go.Indicator(mode="gauge+number", value=roe_25, number={'suffix': "%"}, title={'text': "ROE", 'font': {'size': 14}}, gauge={'axis': {'range': [0, 40]}, 'bar': {'color': "#9467bd"}}))
                fig3.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), template="plotly_dark")
                c3.plotly_chart(fig3, use_container_width=True)

                st.subheader("💡 Expert Financial Diagnosis")
                nb_positifs = ["Excellent cash management. Easily self-finances operations.", "Strong operational profitability confirmed across the board.", "Optimal value creation for shareholders with a highly attractive ROE."]
                nb_negatifs = ["Severe liquidity drain: Imminent risk of short-term insolvency.", "Value destruction: ROE is too low to attract or retain investors.", "Current debt burden is too heavy compared to available liquidity."]
                
                score_positif = sum([current_ratio_25 >= 1.2, net_margin_25 >= 8.0, roe_25 >= 12.0])
                color, status, selected_nbs = ("#2ca02c", "Favorable Financial Situation (Key Strengths)", nb_positifs) if score_positif >= 2 else ("#d62728", "Critical Financial Situation (Vulnerabilities)", nb_negatifs)
                    
                st.markdown(f"""
                <div class="report-box" style="border-color: {color};">
                    <h4 style="color: {color}; margin-top: 0;">{status}</h4>
                    <ul>
                        <li style="color: {color};"><b>N.B:</b> {selected_nbs[0]}</li>
                        <li style="color: {color};"><b>N.B:</b> {selected_nbs[1]}</li>
                        <li style="color: {color};"><b>N.B:</b> {selected_nbs[2]}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # ==============================
            # RIGHT COLUMN (New Features)
            # ==============================
            with right_col:
                st.subheader("🎛️ Sensitivity Analysis (What-If)")
                st.markdown("Adjust parameters to simulate future performance impacts.")
                
                sim_revenue_growth = st.slider("Forecast Revenue Growth / Decline (%)", -30, 30, 0, step=1)
                sim_cost_reduction = st.slider("Simulate Cost Reduction (%)", 0, 20, 0, step=1)
                
                # Simple Simulation Math
                sim_rev = rev_25 * (1 + (sim_revenue_growth/100))
                sim_costs = (rev_25 - net_25) * (1 - (sim_cost_reduction/100))
                sim_net = sim_rev - sim_costs
                sim_margin = (sim_net / sim_rev * 100) if sim_rev > 0 else 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <p style="margin:0; color:#b3b3b3; font-size:14px;">Simulated Revenue (MAD)</p>
                    <h3 style="margin:0; color:#00ff00;">{sim_rev:,.2f}</h3>
                </div>
                <div class="metric-card">
                    <p style="margin:0; color:#b3b3b3; font-size:14px;">Simulated Net Margin</p>
                    <h3 style="margin:0; color:#1f77b4;">{sim_margin:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🏗️ Market Benchmarking Overview")
                sector_pe = df_live['PE_Ratio'].mean() if df_live is not None else 15.0
                st.info(f"**BTP Sector Average P/E Ratio:** {sector_pe:.2f}")
                st.caption("Detailed sector data available in Tab 2.")

                # --- ANIMATED RED PDF DOWNLOAD BUTTON ---
                st.markdown("<br><br>", unsafe_allow_html=True)
                ratios_dict = {"Revenue": f"{rev_25:,.2f} MAD", "Net Margin": f"{net_margin_25:.2f}%", "ROE": f"{roe_25:.2f}%", "Current Ratio": f"{current_ratio_25:.2f}"}
                
                try:
                    pdf_bytes = create_pdf(ratios_dict, selected_nbs, sector_pe, df_display)
                    b64_pdf = base64.b64encode(pdf_bytes).decode('latin-1')
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Financial_Report_Z_ELAIDI.pdf" class="btn-animated-red">📄 Download Complete PDF Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error("Error generating PDF. Please ensure fpdf is in requirements.txt.")

        except Exception as e:
            st.error(f"⚠️ Read Error: Please use the required standard template.")

# ==========================================
# TAB 2, 3, 4: REMAINDER OF APP (Kept identical for stability)
# ==========================================
with tab2:
    st.header(f"🏗️ BTP Sector Live Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Casablanca Time)")
    if df_live is not None:
        def color_variation(val): return f"color: {'#00ff00' if val > 0 else '#ff0000' if val < 0 else 'white'}"
        st.dataframe(df_live[["Company", "Live_Price_MAD", "Variation", "Market_Cap_Billion", "PE_Ratio", "Dividend_Yield"]].style.map(color_variation, subset=['Variation']).highlight_max(axis=0, subset=["Market_Cap_Billion"], color="#1f77b4"), use_container_width=True)
        fig = px.bar(df_live, x="Company", y="Live_Price_MAD", color="Variation", title="Live Stock Prices (MAD) & Intraday Variation", color_continuous_scale="RdYlGn", template="plotly_dark")
        fig.update_layout(dragmode=False, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

with tab3:
    st.header("💹 Technical Analysis & Historical Trends")
    if df_live is not None:
        c_sel1, c_sel2, c_sel3 = st.columns(3)
        with c_sel1: selected_company = st.selectbox("Select Company:", df_live["Company"].tolist())
        with c_sel2: time_period = st.selectbox("Timeframe:", ["1 Month (30 Days)", "3 Months (90 Days)", "6 Months (180 Days)"])
        with c_sel3: chart_type = st.radio("Chart Style:", ["Candlesticks", "Line Chart"], horizontal=True)
        
        num_days = {"1 Month (30 Days)": 30, "3 Months (90 Days)": 90, "6 Months (180 Days)": 180}[time_period]
        base_price = df_live[df_live["Company"] == selected_company]["Live_Price_MAD"].values[0]
        dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=num_days)
        
        np.random.seed(42 + len(selected_company) + num_days)
        vol = base_price * 0.05
        changes = np.random.normal(0, vol, size=num_days)
        closes = base_price - np.cumsum(changes[::-1])[::-1] 
        opens = closes - np.random.normal(0, vol, size=num_days)
        highs = np.maximum(opens, closes) + np.abs(np.random.normal(0, vol*1.2, size=num_days))
        lows = np.minimum(opens, closes) - np.abs(np.random.normal(0, vol*1.2, size=num_days))
        
        if chart_type == "Candlesticks":
            fig_m = go.Figure(data=[go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes, increasing_line_color='#00ff00', decreasing_line_color='#ff0000')])
        else:
            fig_m = go.Figure(data=[go.Scatter(x=dates, y=closes, mode='lines+markers', line=dict(color='#1f77b4', width=2))])
            
        fig_m.update_layout(height=450, title=f"Price Movement - {selected_company}", yaxis_title="Price (MAD)", template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_m, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': True})

with tab4:
    st.header("👤 About the Creator")
    c_abt1, c_abt2 = st.columns([2, 1])
    with c_abt1:
        st.markdown("### **Zakaria Elaidi** | *Financial Analyst*\n\nZakaria is a dedicated financial analyst currently specializing in Finance at the prestigious **Ecole Nationale de Commerce et de Gestion (ENCG) in El Jadida**. \n\nWith a strong background in corporate finance and data analysis, Zakaria operates as a successful freelance financial consultant. He has a proven track record, having delivered over **150 financial modeling and consulting projects** for a global client base.")
        st.info("💡 **Core Expertise:** Equity Research, Corporate Finance, Data Automation, Financial Modeling.")
    with c_abt2:
        st.markdown('<div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; border-top: 4px solid #c1272d;"><h3 style="margin-top:0;">Professional Network</h3><p>Open for financial consulting opportunities, equity research projects, and professional networking.</p><br><a href="https://www.linkedin.com/in/zakaria-elaidi/" target="_blank" style="background-color: #0077b5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Connect on LinkedIn</a></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #a0a0a0; font-size: 15px;'>© 2026 | Automated Financial Analytics Platform | <b>Designed & Built by ELAIDI ZAKARIA</b></div>", unsafe_allow_html=True)
