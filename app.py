import streamlit as st
import pandas as pd
from supabase import create_client, ClientOptions

# MUST BE THE FIRST LINE
st.set_page_config(
    page_title="Z.ELAIDI - Financial Hub", 
    layout="wide", 
    page_icon="📊", 
    initial_sidebar_state="collapsed" 
)

# ==========================================
# 1. SUPABASE SETUP
# ==========================================
try:
    supabase = create_client(
        supabase_url=st.secrets["SUPABASE_URL"],
        supabase_key=st.secrets["SUPABASE_KEY"],
        options=ClientOptions(postgrest_client_timeout=10)
    )
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

# ==========================================
# 2. DYNAMIC CSS & UI HACKS
# ==========================================
# Hack to rename 'app' to '🏠 Home' in the sidebar
st.markdown("""
<style>
    [data-testid="stSidebarNav"] li:first-child a span { display: none !important; }
    [data-testid="stSidebarNav"] li:first-child a::after { content: "🏠 Home"; font-size: 15px; margin-left: 0px; }
    
    /* Global Styles */
    .full-width-banner { position: relative; width: 100%; height: 250px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background-position: center; margin-bottom: 2rem; border-radius: 10px; border-left: 5px solid #c1272d; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.8) 40%, rgba(193,39,45,0.2) 100%); }
    .banner-content { position: absolute; top: 50%; left: 30px; transform: translateY(-50%); z-index: 2; }
    .moroccan-badge { display: inline-block; background: rgba(193,39,45,0.2); border: 1px solid #c1272d; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; margin-top: 15px; font-weight: bold; }
    
    /* Colored Cards */
    .card-blue { background-color: #0e1621; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    .card-green { background-color: #0d1a10; border-left: 4px solid #2ca02c; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    .card-purple { background-color: #1a0f24; border-left: 4px solid #9467bd; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    .card-red { background-color: #240f0f; border-left: 4px solid #d62728; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    .card-orange { background-color: #24180f; border-left: 4px solid #ff7f0e; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    .card-teal { background-color: #0f2424; border-left: 4px solid #17becf; padding: 15px; border-radius: 5px; height: 110px; margin-bottom: 15px; }
    
    .card-title { margin: 0; font-size: 1.1rem; font-weight: bold; }
    .card-text { color: #b3b3b3; font-size: 0.85rem; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

if st.session_state.user is None:
    st.markdown("<style>[data-testid='stSidebar'] { display: none !important; } [data-testid='collapsedControl'] { display: none !important; }</style>", unsafe_allow_html=True)

# ==========================================
# 3. DATA HELPER FOR DASHBOARD
# ==========================================
@st.cache_data(ttl=60)
def get_dashboard_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["PE_Ratio"] = pd.to_numeric(df["PE_Ratio"], errors='coerce')
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        return df
    except: return None

# ==========================================
# 4. ROUTING & UI
# ==========================================
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_info, col_auth = st.columns([1.5, 1], gap="large")
    
    with col_info:
        st.image("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=2070&auto=format&fit=crop", use_container_width=True)
        st.markdown("## 📊 Welcome to Z.ELAIDI Financial Hub")
        st.markdown("<p style='color: #b3b3b3; font-size: 1.1rem;'>An exclusive Equity Research and M&A Valuation platform dedicated to the <b>Moroccan BTP Sector</b>.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        **Platform Capabilities:**
        * 📈 **Corporate Analysis:** Automated variance analysis & financial diagnosis.
        * 🏗️ **Market Benchmark:** Real-time peer comparison (TGCC, LafargeHolcim, etc.).
        * 💼 **M&A Deal Room:** DCF Valuation, LBO modeling, and Monte Carlo Simulations.
        * 📑 **Instant Reporting:** Generate institutional-grade investment teasers (PDF).
        """)
        
    with col_auth:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: white; margin-top: 5px; margin-bottom: 0;'>SYSTEM ACCESS</h3>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 1px solid #c1272d; margin-top: 10px; margin-bottom: 20px; width: 50%; margin-left: auto; margin-right: auto;'>", unsafe_allow_html=True)
            
            choice = st.radio("Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
            email = st.text_input("Corporate Email", placeholder="email@domain.com")
            password = st.text_input("Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Authenticate", use_container_width=True, type="primary"):
                if choice == "Login":
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        st.rerun()
                    except Exception as e: st.error(f"Login Error: Invalid credentials or user not found.")
                else:
                    try:
                        supabase.auth.sign_up({"email": email, "password": password})
                        st.success("Account created successfully! Switch to Login.")
                    except Exception as e: st.error(f"Sign Up Error: {str(e)}")

else:
    # -----------------------------------------------------
    # HOME PAGE DASHBOARD (After Login)
    # -----------------------------------------------------
    st.markdown("""
    <div class="full-width-banner">
        <div class="banner-overlay"></div>
        <div class="banner-content">
            <h1 style="color: white; margin: 0; font-size: 2.8rem; letter-spacing: 1px;">Casablanca Stock Exchange</h1>
            <p style="color:#e0e0e0; font-size:1.3rem; margin: 5px 0 0 0;">BTP Sector Equity Research & Financial Analytics Hub</p>
            <div class="moroccan-badge">🇲🇦 Moroccan Market Focus</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_overview, col_pipeline = st.columns([2, 1], gap="large")
    
    with col_overview:
        st.markdown("### 🌐 Sector Overview (CSE)")
        df_dash = get_dashboard_data()
        
        if df_dash is not None:
            avg_pe = df_dash["PE_Ratio"].mean()
            top_stock = df_dash.loc[df_dash["Price_MAD"].idxmax(), "Company"]
            tracked_count = len(df_dash)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Tracked Companies", f"{tracked_count} Entities")
            m2.metric("Sector Average P/E", f"{avg_pe:.1f}x")
            m3.metric("Highest Priced Stock", top_stock)
            
    with col_pipeline:
        st.markdown("### 🔄 M&A Pipeline")
        st.markdown("""
        <div style="font-size: 0.9rem; color: #d0d3d4;">
        <b>Step 1:</b> Upload Target Financials.<br>
        <b>Step 2:</b> Generate Pitch Teaser.<br>
        <b>Step 3:</b> Run DCF & Monte Carlo.<br>
        <b>Step 4:</b> Save to History Database.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Navigation Modules")
    
    # ROW 1 OF BUTTONS
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""<div class='card-blue'><p class='card-title' style='color:#1f77b4;'>📉 Corporate Analysis</p><p class='card-text'>Upload Excel models and generate investment teasers.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_corp", use_container_width=True): st.switch_page("pages/1_Corporate_Analysis.py")
            
    with c2:
        st.markdown("""<div class='card-green'><p class='card-title' style='color:#2ca02c;'>⚖️ Sector Benchmark</p><p class='card-text'>Compare target operational margins against Moroccan peers.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_bench", use_container_width=True): st.switch_page("pages/2_BTP_Benchmark.py")
            
    with c3:
        st.markdown("""<div class='card-purple'><p class='card-title' style='color:#9467bd;'>💼 M&A Deal Room</p><p class='card-text'>Execute LBO Quick-Models and Monte Carlo DCF simulations.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_ma", use_container_width=True): st.switch_page("pages/3_MA_Valuation.py")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2 OF BUTTONS
    c4, c5, c6 = st.columns(3)
    
    with c4:
        st.markdown("""<div class='card-red'><p class='card-title' style='color:#d62728;'>💹 Live Charts</p><p class='card-text'>Track real-time market trends and historical pricing data.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_charts", use_container_width=True): st.switch_page("pages/4_Live_Charts.py")
            
    with c5:
        st.markdown("""<div class='card-orange'><p class='card-title' style='color:#ff7f0e;'>🗄️ My History</p><p class='card-text'>Access and manage your previously saved analysis sessions.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_hist", use_container_width=True): st.switch_page("pages/6_My_History.py")
            
    with c6:
        st.markdown("""<div class='card-teal'><p class='card-title' style='color:#17becf;'>👤 About Creator</p><p class='card-text'>Professional profile, background, and networking links.</p></div>""", unsafe_allow_html=True)
        if st.button("Access Module ➡️", key="btn_about", use_container_width=True): st.switch_page("pages/5_About_Creator.py")

    st.markdown("---")
    
    # LOGOUT BUTTON
    col_empty, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("🚪 Terminate Session", type="secondary", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
