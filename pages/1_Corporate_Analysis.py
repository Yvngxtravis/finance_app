import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import json
from datetime import datetime
from fpdf import FPDF
from supabase import create_client, ClientOptions

# --- SECURITY ---
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

# --- GLOBAL STATE ---
lang = st.session_state.get("lang", "English")
curr = st.session_state.get("currency", "MAD")
rate = st.session_state.get("rates", {"MAD": 1.0, "USD": 0.10, "EUR": 0.09})[curr]
sym = st.session_state.get("sym", {"MAD": "MAD", "USD": "$", "EUR": "€"})[curr]

# --- TRANSLATION DICTIONARY ---
t = {
    "English": {
        "title": "📈 Corporate Analysis", "upload": "Upload your company's financial Excel template.", "dl_temp": "📥 Download Template",
        "var_title": "📋 Variance Analysis", "sens_title": "🎛️ Sensitivity (What-If)", 
        "rev_growth": "Revenue Growth (%)", "cost_red": "Cost Reduction (%)",
        "sim_rev": "Simulated Revenue", "sim_margin": "Simulated Net Margin",
        "kpi_title": "📊 Key Performance Ratios", "cr": "Current Ratio", "nm": "Net Margin", "roe": "ROE",
        "diag_title": "💡 Expert Diagnosis", "fav": "Favorable Financial Situation", "crit": "Critical Financial Situation",
        "fav_n1": "Excellent liquidity management.", "fav_n2": "Strong operational profitability confirmed.", "fav_n3": "Optimal value creation for shareholders with attractive ROE.",
        "crit_n1": "Potential liquidity drain: Monitor short-term solvency.", "crit_n2": "Value destruction: Margins are below sector standards.", "crit_n3": "High dependency on debt or low operational efficiency.",
        "yoy_title": "📈 YoY Progression", "rev": "Revenue", "net": "Net Income",
        "act_title": "💾 Actions & Reports", "save": "💾 Save to History", "dl_pdf": "📄 Download as a PDF", "dl_xlsx": "📥 Export to Excel",
        "success_save": "✅ Saved successfully!", "fail_save": "⚠️ Failed to save.", "err_file": "⚠️ Error processing file.",
        "pdf_head": "COMPREHENSIVE FINANCIAL REPORT", "pdf_gen": "Generated on", "pdf_s1": "1. Financial Statements Overview & Variance",
        "pdf_col1": "Line Item", "pdf_col2": "YoY Growth (%)", "pdf_s2": "2. Key Performance Indicators",
        "pdf_s3": "3. Scenario & Sensitivity Outlook", "pdf_s4": "4. Expert Diagnosis & Recommendations", "pdf_foot": "Strictly Confidential | M&A Advisory Desk - Z.ELAIDI Financial Hub"
    },
    "Français": {
        "title": "📈 Analyse d'Entreprise", "upload": "Importez le modèle financier Excel de votre entreprise.", "dl_temp": "📥 Télécharger le Modèle",
        "var_title": "📋 Analyse des Écarts", "sens_title": "🎛️ Sensibilité (Simulations)", 
        "rev_growth": "Croissance des Revenus (%)", "cost_red": "Réduction des Coûts (%)",
        "sim_rev": "Revenus Simulés", "sim_margin": "Marge Nette Simulée",
        "kpi_title": "📊 Indicateurs de Performance", "cr": "Ratio de Liquidité", "nm": "Marge Nette", "roe": "ROE",
        "diag_title": "💡 Diagnostic d'Expert", "fav": "Situation Financière Favorable", "crit": "Situation Financière Critique",
        "fav_n1": "Excellente gestion de la liquidité.", "fav_n2": "Forte rentabilité opérationnelle confirmée.", "fav_n3": "Création de valeur optimale pour les actionnaires.",
        "crit_n1": "Risque de liquidité potentiel : Surveillez la solvabilité.", "crit_n2": "Destruction de valeur : Marges inférieures aux normes.", "crit_n3": "Forte dépendance à la dette.",
        "yoy_title": "📈 Progression Annuelle", "rev": "Revenus", "net": "Revenu Net",
        "act_title": "💾 Actions & Rapports", "save": "💾 Sauvegarder dans l'Historique", "dl_pdf": "📄 Télécharger en PDF", "dl_xlsx": "📥 Exporter vers Excel",
        "success_save": "✅ Sauvegardé avec succès !", "fail_save": "⚠️ Échec de la sauvegarde.", "err_file": "⚠️ Erreur de traitement.",
        "pdf_head": "RAPPORT FINANCIER COMPLET", "pdf_gen": "Généré le", "pdf_s1": "1. Aperçu des États Financiers et Écarts",
        "pdf_col1": "Poste", "pdf_col2": "Croissance Annuelle (%)", "pdf_s2": "2. Indicateurs Clés de Performance",
        "pdf_s3": "3. Perspectives de Sensibilité", "pdf_s4": "4. Diagnostic d'Expert", "pdf_foot": "Strictement Confidentiel | Bureau de Conseil M&A"
    },
    "Español": {
        "title": "📈 Análisis Corporativo", "upload": "Sube la plantilla financiera en Excel.", "dl_temp": "📥 Descargar Plantilla",
        "var_title": "📋 Análisis de Variaciones", "sens_title": "🎛️ Sensibilidad (Escenarios)", 
        "rev_growth": "Crecimiento de Ingresos (%)", "cost_red": "Reducción de Costes (%)",
        "sim_rev": "Ingresos Simulados", "sim_margin": "Margen Neto Simulado",
        "kpi_title": "📊 Ratios de Rendimiento", "cr": "Ratio de Liquidez", "nm": "Margen Neto", "roe": "ROE",
        "diag_title": "💡 Diagnóstico de Expertos", "fav": "Situación Financiera Favorable", "crit": "Situación Financiera Crítica",
        "fav_n1": "Excelente gestión de la liquidez.", "fav_n2": "Fuerte rentabilidad operativa.", "fav_n3": "Óptima creación de valor.",
        "crit_n1": "Riesgo de liquidez a corto plazo.", "crit_n2": "Márgenes por debajo de estándares.", "crit_n3": "Alta dependencia de deuda.",
        "yoy_title": "📈 Progresión Interanual", "rev": "Ingresos", "net": "Ingreso Neto",
        "act_title": "💾 Acciones y Reportes", "save": "💾 Guardar en Historial", "dl_pdf": "📄 Descargar como PDF", "dl_xlsx": "📥 Exportar a Excel",
        "success_save": "✅ ¡Guardado exitosamente!", "fail_save": "⚠️ Error al guardar.", "err_file": "⚠️ Error al procesar.",
        "pdf_head": "INFORME FINANCIERO COMPLETO", "pdf_gen": "Generado el", "pdf_s1": "1. Estados Financieros y Variaciones",
        "pdf_col1": "Partida", "pdf_col2": "Crecimiento Interanual (%)", "pdf_s2": "2. Indicadores Clave",
        "pdf_s3": "3. Perspectivas de Sensibilidad", "pdf_s4": "4. Diagnóstico de Expertos", "pdf_foot": "Estrictamente Confidencial | Asesoría M&A"
    },
    "العربية": {
        "title": "📈 تحليل الشركات", "upload": "قم برفع نموذج الإكسل المالي.", "dl_temp": "📥 تنزيل النموذج",
        "var_title": "📋 تحليل التغيرات", "sens_title": "🎛️ تحليل الحساسية (محاكاة)", 
        "rev_growth": "نمو الإيرادات (%)", "cost_red": "تخفيض التكاليف (%)",
        "sim_rev": "الإيرادات المحاكية", "sim_margin": "هامش الربح المحاكى",
        "kpi_title": "📊 مؤشرات الأداء", "cr": "نسبة السيولة", "nm": "هامش الربح الصافي", "roe": "العائد على حقوق المساهمين",
        "diag_title": "💡 تشخيص الخبراء", "fav": "وضع مالي ملائم", "crit": "وضع مالي حرج",
        "fav_n1": "إدارة ممتازة للسيولة.", "fav_n2": "ربحية تشغيلية قوية.", "fav_n3": "خلق قيمة ممتازة للمساهمين.",
        "crit_n1": "استنزاف محتمل للسيولة.", "crit_n2": "هوامش ربح ضعيفة.", "crit_n3": "اعتماد كبير على الديون.",
        "yoy_title": "📈 التطور السنوي", "rev": "الإيرادات", "net": "صافي الدخل",
        "act_title": "💾 الإجراءات والتقارير", "save": "💾 حفظ في السجل", "dl_pdf": "📄 تنزيل كملف PDF", "dl_xlsx": "📥 تصدير إلى Excel",
        "success_save": "✅ تم الحفظ بنجاح!", "fail_save": "⚠️ فشل الحفظ.", "err_file": "⚠️ خطأ في معالجة الملف.",
        "pdf_head": "تقرير مالي مفصل", "pdf_gen": "تاريخ الإنشاء", "pdf_s1": "1. نظرة عامة على القوائم المالية",
        "pdf_col1": "البيان", "pdf_col2": "التطور السنوي (%)", "pdf_s2": "2. مؤشرات الأداء الرئيسية",
        "pdf_s3": "3. تحليل الحساسية", "pdf_s4": "4. تشخيص الخبراء", "pdf_foot": "سري للغاية | مكتب استشارات الاندماج والاستحواذ"
    }
}
txt = t[lang]
pdf_lang = lang if lang != "العربية" else "English"
pdf_txt = t[pdf_lang]

# --- UI CSS ---
st.markdown(f"""
<style>
    .metric-box {{ background-color: #161a22; padding: 15px; border-radius: 8px; border-top: 3px solid #1f77b4; margin-bottom: 15px; text-align: center; }}
    .report-box {{ padding: 20px; border-radius: 10px; background-color: #161a22; border-left: 5px solid; margin-top: 20px; }}
    {'[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stHeader"] { direction: ltr; }' if lang == "العربية" else ''}
</style>
""", unsafe_allow_html=True)

st.title(txt["title"])

# --- VALIDATOR ---
REQUIRED_COLUMNS = ["Revenue", "Net Income", "Current Assets", "Current Liabilities", "Total Equity"]
def validate_excel(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.index]
    return (False, f"Missing: {', '.join(missing)}") if missing else (True, None)

# --- APP LOGIC ---
uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])
if uploaded_file:
    try:
        df_finance = pd.read_excel(uploaded_file, index_col=0)
        df_finance.index = df_finance.index.str.strip()
        is_valid, err = validate_excel(df_finance)
        if not is_valid: st.error(err); st.stop()
        
        col_24, col_25 = df_finance.columns[0], df_finance.columns[1]
        
        # Calculations
        df_display = df_finance.copy()
        df_display[col_24] = pd.to_numeric(df_display[col_24], errors='coerce') * rate
        df_display[col_25] = pd.to_numeric(df_display[col_25], errors='coerce') * rate
        df_display['YoY Growth (%)'] = ((df_display[col_25] - df_display[col_24]) / df_display[col_24]) * 100
        
        # 1. SENSITIVITY HEATMAP
        st.subheader(txt["sens_title"])
        wacc = st.slider("WACC %", 5.0, 15.0, 10.0, 0.5) / 100
        growth = st.slider("Terminal Growth %", 1.0, 5.0, 2.0, 0.5) / 100
        
        # 2. DATA TABLE
        st.dataframe(df_display.style.format({col_24: f"{{:,.0f}} {sym}", col_25: f"{{:,.0f}} {sym}", 'YoY Growth (%)': "{:.2f}%"}), use_container_width=True)
        
        # 3. EXPORT EXCEL
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_display.to_excel(writer, sheet_name="Analysis")
        st.download_button(txt["dl_xlsx"], data=output.getvalue(), file_name="Analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    except Exception as e: st.error(f"{txt['err_file']} {str(e)}")
