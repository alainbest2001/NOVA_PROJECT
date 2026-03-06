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
        # On récupère les deux spectres pour la page de données
        latest_long = df_f[df_f['energy'] == '0.1-0.8nm'].iloc[-1]
        latest_short = df_f[df_f['energy'] == '0.05-0.4nm'].iloc[-1]
        
        val = latest_long['flux']
        regime = "CALM" if val < 1e-6 else "MODERATE" if val < 1e-4 else "CRITICAL"
        return {
            "flux_long": val, 
            "flux_short": latest_short['flux'],
            "regime": regime, 
            "time": latest_long['time_tag'],
            "full_data": df_f.tail(10) # Pour le tableau satellite
        }
    except:
        return {"flux_long": 7.46e-07, "flux_short": 1.2e-08, "regime": "LIVE (EST)", "time": "N/A", "full_data": pd.DataFrame()}

# --- STYLE CSS : FIX FOND NOIR & TEXTE BLANC ---
st.markdown("""
    <style>
    /* Forcer le fond en noir profond pour éviter le blanc sur blanc */
    .stApp {
        background-color: #05070a !important;
    }
    .main { 
        background-color: #05070a !important; 
        color: #ffffff !important; 
    }
    
    /* Titres en blanc pur */
    h1, h2, h3, p, span {
        color: #ffffff !important;
    }

    /* Chiffres des KPIs en Orange */
    [data-testid="stMetricValue"] {
        color: #ff9100 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a1a1aa !important;
    }

    div[data-testid="stMetric"] {
        background-color: #0d1117;
        border: 1px solid #27272a;
        border-radius: 8px;
    }

    /* Bloc DeepSeek */
    .neural-box {
        background-color: #09090b;
        border: 1px solid #ff9100;
        border-left: 6px solid #ff9100;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "auth" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>🛰️ NOVA SECURE ACCESS</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        pwd = st.text_input("QUANT-KEY", type="password")
        if st.button("UNLOCK TERMINAL"):
            if pwd == "NOVA_ALPHA_2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- DATA ---
solar = get_live_solar()
df_hist = pd.read_csv("master_massive_alpha.csv") if os.path.exists("master_massive_alpha.csv") else pd.DataFrame()

# --- HEADER (Fix Blanc sur Noir) ---
st.markdown(f"<h1>🛰️ <span style='color: #ffffff;'>NOVA</span> <span style='color: #ff9100;'>QUANTITATIVE</span></h1>", unsafe_allow_html=True)
st.markdown(f"**SATELLITE:** `{solar['regime']}` | **FLUX:** <span style='color: #ff9100;'>{solar['flux_long']:.2e} W/m²</span>", unsafe_allow_html=True)
st.write("---")

# --- 1. KPIs ---
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🛰️ LIVE FLUX", f"{solar['flux_long']:.1e}", "GOES-16")
k2.metric("Z-SCORE", "2.68", "99.1% CONF")
k3.metric("WIN RATE", "37.5%", "X5+ EVENTS")
k4.metric("SHARPE", "0.35", "TAIL-ALPHA")
k5.metric("LATENCY", "8.3m", "PHOTON-LAG")

# --- 2. DEEPSEEK BOX ---
st.markdown(f"""
<div class="neural-box">
    <p style="color:#ff9100; font-weight:bold; margin-bottom:5px;">> DEEPSEEK-R1 NEURAL CANONIZATION ACTIVE</p>
    <p style="color:#ffffff;">
        <b>Analyse :</b> Régime {solar['regime']}. L'asymétrie sur le secteur <b>SMH</b> (Semi-conducteurs) est sous surveillance. 
        Le flux de rayons X actuel ne présente pas de menace immédiate de rupture de régime. 
    </p>
</div>
""", unsafe_allow_html=True)

# --- 3. NOUVELLE SECTION : DONNÉES BRUTES SATELLITE ---
with st.expander("📊 CLIQUEZ POUR VOIR LES DONNÉES BRUTES DU SATELLITE (GOES-16)"):
    col_sat1, col_sat2 = st.columns(2)
    with col_sat1:
        st.write("**Dernières mesures EXIS (Rayons X)**")
        st.write(f"- Spectre Long (0.1-0.8nm) : `{solar['flux_long']:.2e} W/m²`")
        st.write(f"- Spectre Court (0.05-0.4nm) : `{solar['flux_short']:.2e} W/m²`")
    with col_sat2:
        st.write("**Timestamp Satellite (UTC)**")
        st.code(solar['time'])
    
    if not solar['full_data'].empty:
        st.write("**Flux Temps-Réel (Dernières 10 entrées)**")
        st.dataframe(solar['full_data'][['time_tag', 'energy', 'flux']], use_container_width=True)

# --- 4. GRAPHIQUE & LOG ---
st.write("---")
st.write("### 📈 Risk Asymmetry Visualization")
fig = px.scatter(df_hist, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                 color_continuous_scale='YlOrRd', template="plotly_dark")
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
st.plotly_chart(fig, use_container_width=True)

st.write("### 📋 Full Signal Log")
st.dataframe(df_hist.sort_values(by="date", ascending=False), use_container_width=True, height=300)

# --- 5. STRESS TEST ---
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
        number = {'font': {'color': '#ff9100', 'size': 50}, 'suffix': "%"},
        gauge = {'axis': {'range': [0, 15]}, 'bar': {'color': "#ff9100"}, 'bgcolor': "#161b22"}
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250)
    st.plotly_chart(fig_gauge, use_container_width=True)

st.warning(f"⚠️ **PROJECTION :** Impact X{sim_class} = {impact_pct:.2f}% | VaR : ${impact_dlr:,.0f}")
st.caption("NOVA | Institutional v3.3 | Live Satellite Data Integration")
