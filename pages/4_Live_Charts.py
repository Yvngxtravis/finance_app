import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
        "title": "💹 Live Charts & Market Trends",
        "comp": "Company:", "time": "Timeframe:", "style": "Style:",
        "m1": "1 Month", "m3": "3 Months", "m6": "6 Months",
        "candle": "Candlesticks", "line": "Line Chart",
        "err": "Error loading CSV:", "chart_title": "Price Trend"
    },
    "Français": {
        "title": "💹 Graphiques en Direct et Tendances",
        "comp": "Entreprise :", "time": "Période :", "style": "Style :",
        "m1": "1 Mois", "m3": "3 Mois", "m6": "6 Mois",
        "candle": "Bougies (Candlesticks)", "line": "Courbe (Line)",
        "err": "Erreur de chargement CSV :", "chart_title": "Tendance des Prix"
    },
    "Español": {
        "title": "💹 Gráficos en Vivo y Tendencias",
        "comp": "Empresa:", "time": "Período:", "style": "Estilo:",
        "m1": "1 Mes", "m3": "3 Meses", "m6": "6 Meses",
        "candle": "Velas (Candlesticks)", "line": "Gráfico de Líneas",
        "err": "Error al cargar CSV:", "chart_title": "Tendencia de Precios"
    },
    "العربية": {
        "title": "💹 رسوم بيانية حية واتجاهات السوق",
        "comp": "الشركة:", "time": "الإطار الزمني:", "style": "النمط:",
        "m1": "شهر واحد", "m3": "3 أشهر", "m6": "6 أشهر",
        "candle": "شموع يابانية", "line": "رسم خطي",
        "err": "خطأ في تحميل ملف CSV:", "chart_title": "اتجاه السعر"
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
    {rtl_css}
</style>
""", unsafe_allow_html=True)

st.title(txt["title"])

# --- DATA FETCHING ---
@st.cache_data(ttl=60)
def get_live_market_data():
    try:
        df = pd.read_csv("btp_market_data.csv")
        df["Price_MAD"] = pd.to_numeric(df["Price_MAD"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"{txt['err']} {str(e)}")
        return None

df_live = get_live_market_data()

# --- UI & CHART LOGIC ---
if df_live is not None:
    with st.container(border=True):
        c_sel1, c_sel2, c_sel3 = st.columns(3)
        with c_sel1: selected_company = st.selectbox(txt["comp"], df_live["Company"].tolist())
        with c_sel2: time_period = st.selectbox(txt["time"], [txt["m1"], txt["m3"], txt["m6"]])
        with c_sel3: chart_type = st.radio(txt["style"], [txt["candle"], txt["line"]], horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map the translated time period back to number of days
    days_map = {txt["m1"]: 30, txt["m3"]: 90, txt["m6"]: 180}
    num_days = days_map[time_period]
    
    # Get base price and apply currency rate
    base_price_mad = df_live[df_live["Company"] == selected_company]["Price_MAD"].values[0]
    base_price = base_price_mad * rate 
    
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=num_days)
    
    # Simulate market volatility based on the converted base price
    np.random.seed(42 + len(selected_company) + num_days)
    vol = base_price * 0.05
    changes = np.random.normal(0, vol, size=num_days)
    closes = base_price - np.cumsum(changes[::-1])[::-1] 
    opens = closes - np.random.normal(0, vol, size=num_days)
    highs = np.maximum(opens, closes) + np.abs(np.random.normal(0, vol*1.2, size=num_days))
    lows = np.minimum(opens, closes) - np.abs(np.random.normal(0, vol*1.2, size=num_days))
    
    # Build Plotly Chart
    if chart_type == txt["candle"]:
        fig_m = go.Figure(data=[go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes, increasing_line_color='#00ff00', decreasing_line_color='#ff0000')])
    else:
        fig_m = go.Figure(data=[go.Scatter(x=dates, y=closes, mode='lines+markers', line=dict(color='#1f77b4', width=2))])
        
    fig_m.update_layout(
        height=450, 
        title=f"{txt['chart_title']} - {selected_company} ({time_period})", 
        template="plotly_dark", 
        xaxis_rangeslider_visible=False,
        yaxis_title=f"Price ({sym})"
    )
    st.plotly_chart(fig_m, use_container_width=True)
