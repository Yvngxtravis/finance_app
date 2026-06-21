import streamlit as st
from supabase import create_client, ClientOptions

# MUST BE THE FIRST LINE
st.set_page_config(page_title="Z.ELAIDI - Financial Hub", layout="wide", page_icon="📊")

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
# 2. CSS STYLING
# ==========================================
st.markdown("""
<style>
.full-width-banner { position: relative; width: 100%; height: 250px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background-position: center; margin-bottom: 2rem; border-radius: 10px; border-left: 5px solid #c1272d; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
.banner-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.8) 40%, rgba(193,39,45,0.2) 100%); }
.banner-content { position: absolute; top: 50%; left: 30px; transform: translateY(-50%); z-index: 2; }
.moroccan-badge { display: inline-block; background: rgba(193,39,45,0.2); border: 1px solid #c1272d; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; margin-top: 15px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ROUTING & UI
# ==========================================
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='color: white; border-top: 4px solid #c1272d; padding-top: 15px;'>SYSTEM ACCESS</h2>", unsafe_allow_html=True)
        choice = st.radio("Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        email = st.text_input("Corporate Email", placeholder="email@domain.com")
        password = st.text_input("Password", type="password")

        if st.button("Authenticate", use_container_width=True):
            if choice == "Login":
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.rerun()
                except Exception as e: st.error(f"Login Error: {str(e)}")
            else:
                try:
                    supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Account created! Switch to Login.")
                except Exception as e: st.error(f"Sign Up Error: {str(e)}")
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
    
    st.info("👈 Please select a module from the sidebar menu to begin your analysis.")
    
    if st.sidebar.button("🚪 Terminate Session", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
