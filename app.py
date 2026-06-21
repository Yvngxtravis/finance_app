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
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# ==========================================
# 2. DYNAMIC CSS & UI HACKS
# ==========================================
# Hack to rename 'app' to '🏠 Home' in the sidebar
st.markdown("""
<style>
    [data-testid="stSidebarNav"] li:first-child a span {
        display: none !important;
    }
    [data-testid="stSidebarNav"] li:first-child a::after {
        content: "🏠 Home";
        font-size: 15px;
        margin-left: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Hide sidebar completely if user is NOT logged in
if st.session_state.user is None:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# General Styles
st.markdown("""
<style>
.full-width-banner { position: relative; width: 100%; height: 250px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background-position: center; margin-bottom: 2rem; border-radius: 10px; border-left: 5px solid #c1272d; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
.banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.8) 40%, rgba(193,39,45,0.2) 100%); }
.banner-content { position: absolute; top: 50%; left: 30px; transform: translateY(-50%); z-index: 2; }
.moroccan-badge { display: inline-block; background: rgba(193,39,45,0.2); border: 1px solid #c1272d; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; margin-top: 15px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

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
    except:
        return None

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
        # FIXED LOGIN BOX USING STREAMLIT NATIVE CONTAINER
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
    # NEW HOME PAGE DASHBOARD (After Login)
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
    
    st.markdown("### 🌐 Sector Overview")
    df_dash = get_dashboard_data()
    
    if df_dash is not None:
        avg_pe = df_dash["PE_Ratio"].mean()
        top_stock = df_dash.loc[df_dash["Price_MAD"].idxmax(), "Company"]
        tracked_count = len(df_dash)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Tracked Companies", f"{tracked_count} Entities")
        m2.metric("Sector Average P/E", f"{avg_pe:.1f}x")
        m3.metric("Highest Priced Stock", top_stock)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions & Modules")
    
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        st.info("📉 **Corporate Analysis**\n\nUpload financial models, generate variance reports, and create Investment Teasers.")
    with col_q2:
        st.warning("⚖️ **Sector Benchmark**\n\nCompare operational margins, liquidity, and ROE against market peers.")
    with col_q3:
        st.success("💼 **M&A Deal Room**\n\nExecute LBO Quick-Models, Advanced CAPM, and Monte Carlo DCF simulations.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚪 Terminate Session", type="secondary"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
