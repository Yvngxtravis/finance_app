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
st.markdown("""
<style>
    /* Rename Sidebar 'app' to 'Home' */
    [data-testid="stSidebarNav"] li:first-child a span { display: none !important; }
    [data-testid="stSidebarNav"] li:first-child a::after { content: "🏠 Home"; font-size: 15px; margin-left: 0px; }
    
    /* Global Styles */
    .full-width-banner { position: relative; width: 100%; height: 250px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background-position: center; margin-bottom: 2rem; border-radius: 10px; border-left: 5px solid #c1272d; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.8) 40%, rgba(193,39,45,0.2) 100%); }
    .banner-content { position: absolute; top: 50%; left: 30px; transform: translateY(-50%); z-index: 2; }
    .moroccan-badge { display: inline-block; background: rgba(193,39,45,0.2); border: 1px solid #c1272d; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; margin-top: 15px; font-weight: bold; }
    
    /* Clickable Cards Configuration */
    a { text-decoration: none !important; }
    .nav-card { padding: 20px; border-radius: 8px; height: 130px; margin-bottom: 20px; transition: transform 0.2s ease, box-shadow 0.2s ease; cursor: pointer; }
    .nav-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.4); }
    
    .card-blue { background-color: #0e1621; border-left: 4px solid #1f77b4; }
    .card-green { background-color: #0d1a10; border-left: 4px solid #2ca02c; }
    .card-purple { background-color: #1a0f24; border-left: 4px solid #9467bd; }
    .card-red { background-color: #240f0f; border-left: 4px solid #d62728; }
    .card-orange { background-color: #24180f; border-left: 4px solid #ff7f0e; }
    .card-teal { background-color: #0f2424; border-left: 4px solid #17becf; }
    
    .card-title { margin: 0; font-size: 1.1rem; font-weight: bold; }
    .card-text { color: #b3b3b3; font-size: 0.85rem; margin-top: 8px; line-height: 1.4; }
    
    /* Custom Overview Dashboard */
    .overview-container { display: flex; justify-content: space-around; background-color: #161a22; padding: 20px; border-radius: 8px; border-top: 3px solid #333; margin-bottom: 30px;}
    .overview-item { text-align: center; }
    .overview-label { margin: 0; color: #b3b3b3; font-size: 14px; margin-bottom: 5px; }
    .overview-value { margin: 0; color: white; font-size: 24px; font-weight: bold; }
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
    except Exception: return None

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
                    except Exception: st.error("Login Error: Invalid credentials or user not found.")
                else:
                    try:
                        supabase.auth.sign_up({"email": email, "password": password})
                        st.success("Account created successfully! Switch to Login.")
                    except Exception as e: st.error(f"Sign Up Error: {str(e)}")

else:
    # -----------------------------------------------------
    # CLEAN & MINIMALIST DASHBOARD
    # -----------------------------------------------------
    
    # --- NEW: TOP HEADER & USER OPTIONS ---
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        # Show a personalized welcome message based on the email
        user_name = st.session_state.user.email.split('@')[0].capitalize()
        st.markdown(f"<h4 style='color: #e0e0e0; margin-top: 10px;'>👋 Welcome back, {user_name}</h4>", unsafe_allow_html=True)
    
    with top_col2:
        # Create a dropdown popover for settings
        with st.popover("⚙️ Settings & Profile", use_container_width=True):
            st.markdown("**User Profile**")
            st.write(f"📧 {st.session_state.user.email}")
            st.divider()
            
            st.markdown("**Preferences**")
            st.selectbox("Default Currency", ["MAD (Dirham)", "USD ($)", "EUR (€)"], label_visibility="collapsed")
            st.selectbox("Report Language", ["English", "Français"], label_visibility="collapsed")
            st.divider()
            
            st.markdown("**System**")
            if st.button("📖 Platform Docs", use_container_width=True):
                st.info("Documentation feature coming soon.")
                
            if st.button("🚪 Terminate Session", type="primary", use_container_width=True):
                supabase.auth.sign_out()
                st.session_state.user = None
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
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
    
    # Custom HTML Overview to fix truncation and spacing
    df_dash = get_dashboard_data()
    if df_dash is not None:
        avg_pe = df_dash["PE_Ratio"].mean()
        top_stock = df_dash.loc[df_dash["Price_MAD"].idxmax(), "Company"]
        tracked_count = len(df_dash)
        
        st.markdown(f"""
        <div class="overview-container">
            <div class="overview-item">
                <p class="overview-label">Tracked Companies</p>
                <p class="overview-value">{tracked_count} Entities</p>
            </div>
            <div class="overview-item">
                <p class="overview-label">Sector Average P/E</p>
                <p class="overview-value">{avg_pe:.1f}x</p>
            </div>
            <div class="overview-item">
                <p class="overview-label">Highest Priced Stock</p>
                <p class="overview-value">{top_stock}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Navigation Modules")
    
    # ROW 1 OF CLICKABLE CARDS
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <a href="Corporate_Analysis" target="_self">
            <div class='nav-card card-blue'>
                <p class='card-title' style='color:#1f77b4;'>📉 Corporate Analysis</p>
                <p class='card-text'>Upload Excel models, run variance analysis, and generate investment teasers.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
            
    with c2:
        st.markdown("""
        <a href="BTP_Benchmark" target="_self">
            <div class='nav-card card-green'>
                <p class='card-title' style='color:#2ca02c;'>⚖️ Sector Benchmark</p>
                <p class='card-text'>Compare target operational margins, liquidity, and ROE against Moroccan peers.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
            
    with c3:
        st.markdown("""
        <a href="MA_Valuation" target="_self">
            <div class='nav-card card-purple'>
                <p class='card-title' style='color:#9467bd;'>💼 M&A Deal Room</p>
                <p class='card-text'>Execute LBO Quick-Models, Advanced CAPM, and Monte Carlo DCF simulations.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    # ROW 2 OF CLICKABLE CARDS
    c4, c5, c6 = st.columns(3)
    
    with c4:
        st.markdown("""
        <a href="Live_Charts" target="_self">
            <div class='nav-card card-red'>
                <p class='card-title' style='color:#d62728;'>💹 Live Charts</p>
                <p class='card-text'>Track real-time market trends, volatility, and historical pricing data.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
            
    with c5:
        st.markdown("""
        <a href="My_History" target="_self">
            <div class='nav-card card-orange'>
                <p class='card-title' style='color:#ff7f0e;'>🗄️ My History</p>
                <p class='card-text'>Access, manage, and download your previously saved analysis sessions.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
            
    with c6:
        st.markdown("""
        <a href="About_Creator" target="_self">
            <div class='nav-card card-teal'>
                <p class='card-title' style='color:#17becf;'>👤 About Creator</p>
                <p class='card-text'>Professional profile, academic background, and networking links.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
