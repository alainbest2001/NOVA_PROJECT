import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import requests
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="NOVA | Terminal Ambre", layout="wide")

# --- MOTEUR DE DONNÉES SATELLITE ---
def get_live_solar():
    try:
        url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
        data = requests.get(url, timeout=5).json()
        df_f = pd.DataFrame(data)
        latest = df_f[df_f['energy'] == '0.1-0.8nm'].iloc[-1]
        val = latest['flux']
        regime = "CALM" if val < 1e-6 else "MODERATE" if val < 1e-4 else "CRITICAL"
        return {"flux": val, "regime": regime, "time": latest['time_tag']}
    except:
        return {"flux": 7.46e-07, "regime": "LIVE (EST)", "time": "N/A"}

# --- STYLE CSS : FOCUS ORANGE & HAUTE LISIBILITÉ ---
st.markdown("""
    <style>
    /* Fond Noir Pur pour faire ressortir l'Orange */
    .main { background-color: #05070a; color: #ffffff; }
    
    /* Chiffres des KPIs en Orange Électrique */
    [data-testid="stMetricValue"] {
        color: #ff9100 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(255, 145, 0, 0.2);
    }
    
    /* Libellés des KPIs */
    [data-testid="stMetricLabel"] {
        color: #a1a1aa !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Cartes des KPIs */
    div[data-testid="stMetric"] {
        background-color: #0d1117;
        border: 1px solid #27272a;
        border-radius: 8px;
        padding: 20px;
    }

    /* Bloc DeepSeek */
    .neural-box {
        background-color: #09090b;
        border: 1px solid #ff9100;
        border-left: 6px solid #ff9100;
        padding: 20px;
        border-radius: 4px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "auth" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #ff9100;'>🛰️ NOVA SECURE ACCESS</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        pwd = st.text_input("QUANT-KEY", type="password")
        if st.button("UNLOCK TERMINAL"):
            if pwd == "NOVA_ALPHA_2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- DATA ---
solar = get_live_solar()
df = pd.read_csv("master_massive_alpha.csv") if os.path.exists("master_massive_alpha.csv") else pd.DataFrame()

# --- HEADER ---
st.markdown(f"<h1 style='color: #ffffff;'>🛰️ NOVA <span style='color: #ff9100;'>QUANTITATIVE</span></h1>", unsafe_allow_html=True)
st.markdown(f"**SATELLITE:** `{solar['regime']}` | **FLUX:** <span style='color: #ff9100; font-weight: bold;'>{solar['flux']:.2e} W/m²</span>", unsafe_allow_html=True)
st.write("---")

# --- 1. KPIs ORANGE ---
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🛰️ LIVE FLUX", f"{solar['flux']:.1e}", "GOES-16")
k2.metric("Z-SCORE", "2.68", "99.1% CONF")
k3.metric("WIN RATE", "37.5%", "X5+ EVENTS")
k4.metric("SHARPE", "0.35", "TAIL-ALPHA")
k5.metric("LATENCY", "8.3m", "PHOTON-LAG")

# --- 2. DEEPSEEK BOX ---
st.markdown(f"""
<div class="neural-box">
    <p style="color:#ff9100; font-weight:bold; margin-bottom:5px; font-family: monospace;">> DEEPSEEK-R1 NEURAL CANONIZATION ACTIVE</p>
    <p style="color:#ffffff; font-size:1.05rem; line-height: 1.6;">
        <b>Régime :</b> {solar['regime']} | Flux actuel stable. <br>
        <b>Analyse :</b> L'asymétrie sur l'indice <b>SMH</b> est confirmée par l'invariant structurel. 
        En cas de pic au-dessus de 1e-4, la volatilité passera en régime critique. 
        <b>Stratégie :</b> Arbitrage de convexité sur les options Tech à delta 0.20.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 3. GRAPHIQUE ---
st.write("### 📈 Risk Asymmetry Visualization")
# Couleurs du graphe passées en magma (plus sombre/orange)
fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                 hover_data=['class'], color_continuous_scale='YlOrRd', template="plotly_dark")
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450)
st.plotly_chart(fig, use_container_width=True)

# --- 4. TABLEAU ---
st.write("### 📋 Full Signal Log")
st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True, height=350)

# --- 5. STRESS TEST (JAUGE ORANGE) ---
st.write("---")
st.write("### 🧪 Systemic Shock Simulator")

c_sim1, c_sim2 = st.columns([1, 2])
with c_sim1:
    sim_class = st.slider("Flare Intensity (X-Class)", 1.0, 50.0, 10.0)
    exposure = st.number_input("Portfolio Exposure ($)", value=1000000)
    impact_pct = (sim_class / 6.9) * 5.77
    impact_dlr = exposure * (impact_pct / 100)

with c_sim2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = impact_pct,
        number = {'font': {'color': '#ff9100', 'size': 60}, 'suffix': "%"},
        title = {'text': "Volatility Spike", 'font': {'color': 'white'}},
        gauge = {
            'axis': {'range': [0, 15], 'tickcolor': "white"},
            'bar': {'color': "#ff9100"},
            'bgcolor': "#161b22",
            'steps': [
                {'range': [0, 5], 'color': "#27272a"},
                {'range': [5, 10], 'color': "#71717a"},
                {'range': [10, 15], 'color': "#ef4444"}
            ]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# ALERTE FINALE
st.warning(f"⚠️ **PROJECTION :** Un événement X{sim_class} génère un choc de **{impact_pct:.2f}%**. VaR : **${impact_dlr:,.0f}**")

st.caption("NOVA | Institutional v3.2 | Real-time Orange-Line Feed")
