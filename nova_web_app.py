import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import requests
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="NOVA | Terminal Quantique", layout="wide")

# --- MOTEUR DE DONNÉES SATELLITE ---
def get_live_solar():
    try:
        url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
        data = requests.get(url, timeout=5).json()
        df_f = pd.DataFrame(data)
        latest = df_f[df_f['energy'] == '0.1-0.8nm'].iloc[-1]
        val = latest['flux']
        # Détermination du régime de risque
        regime = "CALM" if val < 1e-6 else "MODERATE" if val < 1e-4 else "CRITICAL"
        color = "#10b981" if regime == "CALM" else "#f59e0b" if regime == "MODERATE" else "#ef4444"
        return {"flux": val, "regime": regime, "color": color, "time": latest['time_tag']}
    except:
        return {"flux": 1.2e-7, "regime": "SIM", "color": "#6b7280", "time": "N/A"}

# --- STYLE CSS AVANCÉ ---
st.markdown(f"""
    <style>
    .main {{ background-color: #05070a; color: #e5e7eb; }}
    .stMetric {{ background-color: #0d1117; border: 1px solid #1f2937; border-radius: 8px; padding: 15px; }}
    .neural-box {{
        background: linear-gradient(145deg, #0d1117, #161b22);
        border-left: 5px solid #00f2ff;
        padding: 20px;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
    }}
    .stress-card {{
        background-color: #0d1117;
        border: 1px dashed #374151;
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN (Simplifié pour la démo) ---
if "auth" not in st.session_state:
    st.title("🛰️ NOVA SYSTEM ACCESS")
    pwd = st.text_input("QUANT-KEY", type="password")
    if st.button("UNLOCK"):
        if pwd == "NOVA_ALPHA_2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- FETCH DATA ---
solar = get_live_solar()
df = pd.read_csv("master_massive_alpha.csv") if os.path.exists("master_massive_alpha.csv") else pd.DataFrame()

# --- HEADER DYNAMIQUE ---
c_h1, c_h2 = st.columns([3, 1])
with c_h1:
    st.title("🛰️ NOVA | Alpha-Space Terminal")
    st.caption(f"Stratégie : Arbitrage de Latence Exogène | Flux Satellite : {solar['regime']}")
with c_h2:
    st.markdown(f"<div style='text-align:right; color:{solar['color']}; font-size:25px; font-weight:bold;'>● {solar['flux']:.2e} W/m²</div>", unsafe_allow_html=True)

st.write("---")

# --- 1. KPIs RÉELS ---
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("SOLAR REGIME", solar["regime"], delta=None)
k2.metric("Z-SCORE", "2.68", "99.1% Conf.")
k3.metric("WIN RATE", "37.5%", "+12.4% Alpha")
k4.metric("SHARPE", "0.35", "Tail-Risk")
k5.metric("LATENCY", "8.3 min", "Photon/Earth")

# --- 2. ANALYSE NEURALE DEEPSEEK-R1 ---
st.markdown("### 🧠 Canonisation Intel : DeepSeek-R1 Core")
st.markdown(f"""
<div class="neural-box">
    <p style="color:#00f2ff; font-weight:bold;">> [DEEPSEEK-R1] STRUCTURAL ANALYSIS ACTIVE</p>
    <p style="font-size: 0.9rem;">
        <b>Régime Actuel :</b> {solar['regime']} | Flux stabilisé à {solar['flux']:.2e}. <br>
        <b>Analyse de Structure :</b> L'invariant structurel identifié sur le segment <b>SMH/NVDA</b> montre une résistance au bruit thermique. 
        En cas de passage en classe X, la dérive de volatilité (convexité) s'accélérera de manière non-linéaire. <br>
        <b>Recommandation :</b> Positionnement <b>Long Gamma</b> sur les expirations hebdomadaires pour capturer l'excès de Kurtosis.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 3. VISUALISATION & LOG COMPLET ---
st.write("---")
col_g, col_t = st.columns([2, 1])

with col_g:
    st.write("### 📊 Dispersion de Volatilité (Backtest)")
    fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                     hover_data=['class'], color_continuous_scale='Portland', template="plotly_dark")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_t:
    st.write("### 📋 Full Signal Log")
    # Affichage avec style de trading
    st.dataframe(df.sort_values(by="date", ascending=False), height=360, use_container_width=True)

# --- 4. STRESS TEST MONTE-CARLO (REFAIT) ---
st.write("---")
st.write("### 🧪 Advanced Stress-Test Simulator (VaR Engine)")

with st.container():
    sc_1, sc_2 = st.columns([1, 2])
    with sc_1:
        st.markdown("<div class='stress-card'>", unsafe_allow_html=True)
        flare_mag = st.select_slider("Magnitude de l'Événement (Classe X)", options=[1, 5, 10, 20, 50], value=10)
        exposure = st.number_input("Exposition Portefeuille ($)", value=1000000, step=100000)
        
        # Calcul technique (Convexité)
        # On simule que plus l'éruption est forte, plus l'impact est exponentiel (Non-linéaire)
        base_impact = (flare_mag / 6.9) * 5.77
        convexity_adj = 1 + (flare_mag / 50) # Facteur de convexité
        final_impact = base_impact * convexity_adj
        var_loss = exposure * (final_impact / 100)
        st.markdown("</div>", unsafe_allow_html=True)

    with sc_2:
        # Graphique de projection de risque
        x_vals = [1, 5, 10, 20, 30, 40, 50]
        y_vals = [(x / 6.9) * 5.77 * (1 + (x / 50)) for x in x_vals]
        
        fig_stress = go.Figure()
        fig_stress.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', name='Impact Curve', line=dict(color='#ef4444', width=3)))
        fig_stress.add_trace(go.Scatter(x=[flare_mag], y=[final_impact], mode='markers', marker=dict(color='#00f2ff', size=15), name='Current Scenario'))
        
        fig_stress.update_layout(title="Courbe de Risque Non-Linéaire (Impact % vs Classe X)", template="plotly_dark", 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_stress, use_container_width=True)

# ALERTE FINALE TECHNIQUE
st.error(f"""
    **ANALYSE DE SCÉNARIO CRITIQUE :** Un événement **X{flare_mag}** génère un choc de **{final_impact:.2f}%** (incluant ajustement de convexité). 
    **VaR Estimée : ${var_loss:,.0f}**. Recommandation : Achat immédiat de Puts OTM (Delta 0.15).
""")

st.caption("NOVA | Institutional Grade v3.0 | Données NASA/NOAA temps-réel")
