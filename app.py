import streamlit as st
from supabase import create_client, ClientOptions

# MUST BE THE FIRST LINE - Added "collapsed" state
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
# 2. DYNAMIC CSS (Hide Sidebar on Login)
# ==========================================
# Hide sidebar completely if user is NOT logged in
if st.session_state.user is None:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
.full-width-banner { position: relative; width: 100%; height: 250px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background-position: center; margin-bottom: 2rem; border-radius: 10px; border-left: 5px solid #c1272d; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
.banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.8) 40%, rgba(193,39,45,0.2) 100%); }
.banner-content { position: absolute; top: 50%; left: 30px; transform: translateY(-50%); z-index: 2; }
.moroccan-badge { display: inline-block; background: rgba(193,39,45,0.2); border: 1px solid #c1272d; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; margin-top: 15px; font-weight: bold; }
.login-box { padding: 30px; background-color: #161a22; border-radius: 10px; border-top: 4px solid #c1272d; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ROUTING & UI
# ==========================================
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Split the screen into two columns
    col_info, col_auth = st.columns([1.5, 1], gap="large")
    
    with col_info:
        # The presentation side (Image + Info)
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
        # The login side
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white; margin-top: 0;'>SYSTEM ACCESS</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
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
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # WELCOME DASHBOARD (Only visible when logged in)
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
    
    st.info("👈 Please click the arrow icon (top left) to open the menu and begin your analysis.")
    
    if st.button("🚪 Terminate Session", type="primary"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
