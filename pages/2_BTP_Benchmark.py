import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- SECURITY ---
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

# --- GLOBAL STATE INITIALIZATION ---
lang = st.session_state.get("lang", "English")
curr = st.session_state.get("currency", "MAD")
rates = st.session_state.get("rates", {"MAD": 1.0, "USD": 0.10, "EUR": 0.09})
syms = st.session_state.get("sym", {"MAD": "MAD", "USD": "$", "EUR": "€"})

rate = rates[curr]
sym = syms[curr]

# --- TRANSLATION DICTIONARY ---
t = {
    "English": {
        "banner_h": "🏗️ BTP Sector Benchmark", "banner_p": "Compare your target company against Casablanca Stock Exchange peers.",
        "target_title": "🎯 Configure Target Data", "proj_name": "Project Name", "nm": "Net Margin (%)", "roe": "ROE (%)",
        "gearing": "Gearing (Debt/Equity %)", "pe": "Implied P/E Ratio", "help_gearing": "BTP average is ~80%.",
        "info_update": "💡 Charts and tables update automatically.", "data_title": "📊 Market Data Overview",
        "p1_title": "⚖️ 1. Peer Comparison: Profitability & Returns", "select_peers": "Select Competitors to Compare:",
        "p2_title": "⚠️ 2. BTP Risk/Reward Matrix", "p2_desc": "Compares Profitability (ROE) vs Financial Risk (Gearing).",
        "p3_title": "🕸️ 3. 360° Sector Profile", "p3_desc": "Radar chart comparing your target against the market average.",
        "col_price": f"Price ({sym})", "your_target": "Your Target", "market_peer": "Market Peer"
    },
    "Français": {
        "banner_h": "🏗️ Benchmark du Secteur BTP", "banner_p": "Comparez votre entreprise cible avec ses pairs de la Bourse de Casablanca.",
        "target_title": "🎯 Configurer les Données Cibles", "proj_name": "Nom du Projet", "nm": "Marge Nette (%)", "roe": "ROE (%)",
        "gearing": "Gearing (Dette/Capitaux Propres %)", "pe": "Ratio P/E Implicite", "help_gearing": "La moyenne du BTP est d'environ 80%.",
        "info_update": "💡 Les graphiques et tableaux se mettent à jour automatiquement.", "data_title": "📊 Aperçu des Données du Marché",
        "p1_title": "⚖️ 1. Comparaison: Rentabilité & Rendements", "select_peers": "Sélectionnez les concurrents à comparer :",
        "p2_title": "⚠️ 2. Matrice Risque/Rendement BTP", "p2_desc": "Compare la Rentabilité (ROE) au Risque Financier (Gearing).",
        "p3_title": "🕸️ 3. Profil Sectoriel à 360°", "p3_desc": "Graphique radar comparant votre cible à la moyenne du marché.",
        "col_price": f"Prix ({sym})", "your_target": "Votre Cible", "market_peer": "Pair du Marché"
    },
    "Español": {
        "banner_h": "🏗️ Benchmark del Sector BTP", "banner_p": "Compara tu empresa objetivo con sus pares de la Bolsa de Casablanca.",
        "target_title": "🎯 Configurar Datos Objetivo", "proj_name": "Nombre del Proyecto", "nm": "Margen Neto (%)", "roe": "ROE (%)",
        "gearing": "Gearing (Deuda/Capital %)", "pe": "Ratio P/E Implícito", "help_gearing": "El promedio de BTP es ~80%.",
        "info_update": "💡 Los gráficos y tablas se actualizan automáticamente.", "data_title": "📊 Resumen de Datos del Mercado",
        "p1_title": "⚖️ 1. Comparación: Rentabilidad y Retornos", "select_peers": "Selecciona competidores para comparar:",
        "p2_title": "⚠️ 2. Matriz de Riesgo/Recompensa BTP", "p2_desc": "Compara Rentabilidad (ROE) vs Riesgo Financiero (Gearing).",
        "p3_title": "🕸️ 3. Perfil Sectorial 360°", "p3_desc": "Gráfico de radar que compara tu objetivo con el promedio del mercado.",
        "col_price": f"Precio ({sym})", "your_target": "Tu Objetivo", "market_peer": "Par del Mercado"
    },
    "العربية": {
        "banner_h": "🏗️ مقارنة أداء قطاع البناء", "banner_p": "قارن شركتك المستهدفة مع نظيراتها في بورصة الدار البيضاء.",
        "target_title": "🎯 إعداد بيانات الشركة المستهدفة", "proj_name": "اسم المشروع", "nm": "هامش الربح الصافي (%)", "roe": "العائد على حقوق المساهمين (%)",
        "gearing": "الرافعة المالية (الديون/حقوق الملكية %)", "pe": "مكرر الربحية الضمني", "help_gearing": "متوسط القطاع حوالي 80%.",
        "info_update": "💡 يتم تحديث الرسوم البيانية والجداول تلقائيًا.", "data_title": "📊 نظرة عامة على بيانات السوق",
        "p1_title": "⚖️ 1. مقارنة الأقران: الربحية والعوائد", "select_peers": "اختر المنافسين للمقارنة:",
        "p2_title": "⚠️ 2. مصفوفة المخاطر والمكافآت", "p2_desc": "يقارن الربحية مقابل المخاطر المالية (الرافعة المالية).",
        "p3_title": "🕸️ 3. ملف تعريف القطاع 360 درجة", "p3_desc": "رسم بياني راداري يقارن شركتك مع متوسط السوق.",
        "col_price": f"السعر ({sym})", "your_target": "شركتك المستهدفة", "market_peer": "منافس في السوق"
    }
}
txt = t[lang]

# --- UI STYLING & CSS HACKS ---
rtl_css = ""
if lang == "العربية":
    rtl_css = """
    .block-container { direction: rtl; text-align: right; }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"], [data-testid="stHeader"] { direction: ltr !important; text-align: left !important; }
    """

st.markdown(f"""
<style>
    [data-testid="stSidebarNav"] li:first-child a span {{ display: none !important; }}
    [data-testid="stSidebarNav"] li:first-child a::after {{ content: "🏠 Home"; font-size: 15px; margin-left: 0px; }}
    .banner {{ background: linear-gradient(90deg, #0e1621 0%, #1f77b4 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2ca02c; }}
    .banner h1 {{ color: white; margin: 0; font-size: 2rem; }}
    .banner p {{ color: #e0e0e0; margin: 0; font-size: 1rem; }}
    {rtl_css}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="banner" {'dir="rtl"' if lang=="العربية" else ''}>
    <h1>{txt['banner_h']}</h1>
    <p>{txt['banner_p']}</p>
</div>
""", unsafe_allow_html=True)

# --- FETCH MARKET DATA & APPLY CURRENCY ---
@st.cache_data(ttl=60)
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        df["PE_Ratio"] = pd.to_numeric(df["PE_Ratio"], errors='coerce')
        np.random.seed(42)
        df["Net_Margin_%"] = np.random.uniform(5, 18, len(df)).round(2)
        df["ROE_%"] = np.random.uniform(10, 25, len(df)).round(2)
        df["Gearing_%"] = np.random.uniform(30, 150, len(df)).round(2) 
        return df
    except Exception: 
        data = {
            "Company": ["TGCC", "LafargeHolcim", "Addoha", "Alliances", "Sonasid", "Ciments du Maroc"],
            "Price_MAD": [300, 1800, 25, 120, 700, 1500],
            "PE_Ratio": [15, 18, 12, 10, 14, 16],
            "Net_Margin_%": [12.5, 16.0, 8.5, 9.0, 6.5, 15.2],
            "ROE_%": [18.5, 22.0, 14.0, 15.5, 10.0, 20.1],
            "Gearing_%": [85.0, 45.0, 120.0, 135.0, 30.0, 40.0]
        }
        return pd.DataFrame(data)

df_live = get_live_market_data().copy()
df_live["Type"] = txt["market_peer"]

# Apply currency rate
df_live["Price_Converted"] = df_live["Price_MAD"] * rate

# --- TARGET INPUTS IN MAIN PAGE ---
st.markdown(f"### {txt['target_title']}")
with st.container(border=True):
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        target_name = st.text_input(txt["proj_name"], "Project Alpha")
    with col_in2:
        target_margin = st.number_input(txt["nm"], value=14.0, step=0.5)
    with col_in3:
        target_roe = st.number_input(txt["roe"], value=20.0, step=0.5)
        
    col_in4, col_in5, col_in6 = st.columns(3)
    with col_in4:
        target_gearing = st.number_input(txt["gearing"], value=60.0, step=5.0, help=txt["help_gearing"])
    with col_in5:
        target_pe = st.number_input(txt["pe"], value=13.0, step=0.5)
    with col_in6:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(txt["info_update"])

# Append Target to Dataframe
target_row = pd.DataFrame([{
    "Company": target_name, "Price_Converted": 0, "PE_Ratio": target_pe, 
    "Net_Margin_%": target_margin, "ROE_%": target_roe, 
    "Gearing_%": target_gearing, "Type": txt["your_target"]
}])
df_combined = pd.concat([target_row, df_live], ignore_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- RAW DATA TABLE ---
st.subheader(txt["data_title"])

def highlight_target(row):
    if row['Type'] == txt["your_target"]: return ['background-color: rgba(245, 176, 65, 0.15)'] * len(row)
    return [''] * len(row)

# Format the dataframe columns for display
display_table = df_combined[["Company", "Type", "Price_Converted", "PE_Ratio", "Net_Margin_%", "ROE_%", "Gearing_%"]].rename(
    columns={"Price_Converted": txt["col_price"]}
)

st.dataframe(
    display_table.style.apply(highlight_target, axis=1).format({
        txt["col_price"]: "{:,.2f}",
        "PE_Ratio": "{:.2f}x",
        "Net_Margin_%": "{:.2f}%",
        "ROE_%": "{:.2f}%",
        "Gearing_%": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# --- THE UI (CHARTS) ---
st.subheader(txt["p1_title"])
peers = st.multiselect(txt["select_peers"], df_live["Company"].tolist(), default=df_live["Company"].tolist()[:4])

if peers:
    display_df = df_combined[(df_combined["Company"].isin(peers)) | (df_combined["Company"] == target_name)].copy()
    color_map = {target_name: "#f5b041"}
    for peer in peers: color_map[peer] = "#1f77b4"

    col_bar1, col_bar2 = st.columns(2)
    with col_bar1:
        fig_margin = px.bar(display_df, x="Company", y="Net_Margin_%", color="Company", color_discrete_map=color_map, title=txt["nm"])
        fig_margin.update_layout(template="plotly_dark", showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_margin, use_container_width=True)
        
    with col_bar2:
        fig_roe = px.bar(display_df, x="Company", y="ROE_%", color="Company", color_discrete_map=color_map, title=txt["roe"])
        fig_roe.update_layout(template="plotly_dark", showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_roe, use_container_width=True)

st.markdown("---")

# --- BTP RISK MATRIX & SPIDER WEB ---
col_matrix, col_radar = st.columns([1.2, 1], gap="large")

with col_matrix:
    st.subheader(txt["p2_title"])
    st.markdown(f"<p style='color:#b3b3b3; font-size:0.9rem;'>{txt['p2_desc']}</p>", unsafe_allow_html=True)
    
    fig_scatter = px.scatter(
        df_combined, x="Gearing_%", y="ROE_%", color="Type", text="Company", size_max=60,
        color_discrete_map={txt["your_target"]: "#f5b041", txt["market_peer"]: "#1f77b4"}
    )
    fig_scatter.update_traces(textposition='top center', marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
    
    avg_gearing = df_live["Gearing_%"].mean()
    avg_roe = df_live["ROE_%"].mean()
    fig_scatter.add_hline(y=avg_roe, line_dash="dash", line_color="gray", annotation_text="Avg ROE")
    fig_scatter.add_vline(x=avg_gearing, line_dash="dash", line_color="gray", annotation_text="Avg Debt")
    
    fig_scatter.update_layout(template="plotly_dark", xaxis_title=txt["gearing"], yaxis_title=txt["roe"], height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_radar:
    st.subheader(txt["p3_title"])
    st.markdown(f"<p style='color:#b3b3b3; font-size:0.9rem;'>{txt['p3_desc']}</p>", unsafe_allow_html=True)
    
    categories = ['Net Margin', 'ROE', 'P/E Ratio', 'Financial Health']
    
    target_health = max(0, 150 - target_gearing) 
    market_health = max(0, 150 - df_live["Gearing_%"].mean())
    
    target_vals = [target_margin, target_roe, target_pe, target_health]
    market_vals = [df_live["Net_Margin_%"].mean(), df_live["ROE_%"].mean(), df_live["PE_Ratio"].mean(), market_health]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=target_vals, theta=categories, fill='toself', name=txt["your_target"], line_color='#f5b041'))
    fig_radar.add_trace(go.Scatterpolar(r=market_vals, theta=categories, fill='toself', name=txt["market_peer"], line_color='#1f77b4'))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(max(target_vals), max(market_vals)) + 5])),
        showlegend=True, template="plotly_dark", height=450, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
