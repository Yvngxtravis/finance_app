import streamlit as st

# MUST BE THE FIRST LINE
st.set_page_config(page_title="Z.ELAIDI - Financial Analytics", layout="wide", page_icon="📊")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io
import json
import base64
from fpdf import FPDF
from supabase import create_client, ClientOptions

# ==========================================
# 1. SUPABASE CONFIGURATION
# ==========================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

try:
    supabase = create_client(
        supabase_url=SUPABASE_URL,
        supabase_key=SUPABASE_KEY,
        options=ClientOptions(postgrest_client_timeout=10)
    )
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    st.stop()

ADMIN_EMAIL = "zakariaelaidi2006@gmail.com"

if "user" not in st.session_state:
    st.session_state.user = None
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# ==========================================
# 2. TRANSLATION DICTIONARY (i18n)
# ==========================================
t = {
    "English": {
        "tab1": "📈 Corporate Analysis", "tab2": "🏗️ BTP Benchmark", "tab3": "💼 M&A Valuation",
        "tab4": "💹 Live Charts", "tab5": "👤 About Creator", "tab6": "🗄️ My History",
        "upload_msg": "Upload your company's financial Excel template.",
        "dl_btn": "📥 Download Template", "logout": "🚪 Terminate Session",
        "mna_title": "💼 M&A & Private Equity Deal Room", "history_title": "🗄️ Database Records",
        "about_title": "👤 Administrator Profile"
    },
    "Français": {
        "tab1": "📈 Analyse Financière", "tab2": "🏗️ Benchmark BTP", "tab3": "💼 Valorisation M&A",
        "tab4": "💹 Graphiques en Direct", "tab5": "👤 À Propos", "tab6": "🗄️ Mon Historique",
        "upload_msg": "Téléchargez votre modèle financier Excel.",
        "dl_btn": "📥 Télécharger le Modèle", "logout": "🚪 Se Déconnecter",
        "mna_title": "💼 Salle des Transactions M&A et Private Equity", "history_title": "🗄️ Enregistrements",
        "about_title": "👤 Profil Administrateur"
    },
    "Español": {
        "tab1": "📈 Análisis Corporativo", "tab2": "🏗️ Benchmark BTP", "tab3": "💼 Valoración M&A",
        "tab4": "💹 Gráficos en Vivo", "tab5": "👤 Sobre el Creador", "tab6": "🗄️ Mi Historial",
        "upload_msg": "Sube tu plantilla financiera en Excel.",
        "dl_btn": "📥 Descargar Plantilla", "logout": "🚪 Cerrar Sesión",
        "mna_title": "💼 Sala de Fusiones y Adquisiciones", "history_title": "🗄️ Registros de Base de Datos",
        "about_title": "👤 Perfil del Administrador"
    },
    "Arabic": {
        "tab1": "📈 التحليل المالي", "tab2": "🏗️ مقارنة قطاع البناء", "tab3": "💼 تقييم الاستحواذ",
        "tab4": "💹 رسوم بيانية حية", "tab5": "👤 عن المطور", "tab6": "🗄️ سجلي",
        "upload_msg": "قم بتحميل قالب الإكسيل المالي الخاص بشركتك.",
        "dl_btn": "📥 تحميل القالب", "logout": "🚪 تسجيل الخروج",
        "mna_title": "💼 غرفة صفقات الدمج والاستحواذ", "history_title": "🗄️ السجلات المحفوظة",
        "about_title": "👤 الملف الشخصي للمسؤول"
    }
}
lang_dict = t[st.session_state.lang]

# ==========================================
# 3. PRO CSS STYLING
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.admin-badge { background-color: #c1272d; color: white; padding: 3px 8px; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; border-radius: 4px; display: inline-block; margin-left: 10px; }
.sidebar-user { background-color: #161a22; padding: 15px; border-radius: 8px; border-left: 3px solid #1f77b4; margin-bottom: 20px; word-wrap: break-word;}
.ma-card { background-color: #161a22; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-top: 15px; }
.ma-card-title { color: #b3b3b3; font-size: 0.9rem; margin-bottom: 5px; }
.ma-card-value { color: white; font-size: 1.5rem; font-weight: bold; margin: 0; }
.btn-pdf { background-color: #c1272d; color: white !important; padding: 15px 15px; text-align: center; display: block; border-radius: 5px; text-decoration: none !important; font-weight: bold; margin-top: 15px; transition: 0.3s; }
.btn-pdf:hover { background-color: #a02025; color: white !important; text-decoration: none !important; }
.glossary-box { background-color: #0e1117; padding: 15px; border-left: 3px solid #f5b041; border-radius: 5px; font-size: 0.9rem; color: #d0d3d4; margin-bottom: 15px; }
.report-box { padding: 20px; border-radius: 10px; background-color: #161a22; border-left: 5px solid; margin-top: 20px; }
.metric-box { background-color: #161a22; padding: 15px; border-radius: 8px; border-top: 3px solid #1f77b4; margin-bottom: 15px; text-align: center; }

/* NEW BANNER CSS */
.full-width-banner { position: relative; width: 100%; height: 220px; background-image: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'); background-size: cover; background
