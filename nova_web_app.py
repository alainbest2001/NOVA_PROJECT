import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="NOVA | Terminal Alpha", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DESIGN ULTRA-CLARITY (CSS Corrigé) ---
st.markdown("""
    <style>
    /* Fond principal plus doux pour les yeux */
    .main { 
        background-color: #0b0e11; 
        color: #f0f2f6;
    }
    
    /* Cartes de métriques : Contraste maximal */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 20px;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #c9d1d9 !important;
    }

    /* Bloc NOVA Intelligence (Clarifié) */
    .stAlert {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #58a6ff !important;
    }
    
    /* Simulateur de Stress : Texte Blanc sur fond sombre net */
    .stSlider label, .stNumberInput label {
        color: #ffffff !important;
        font-weight: bold;
    }

    /* Tableaux : Fond sombre, texte clair */
    .stDataFrame {
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ACCÈS ---
if "password_correct" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: white;'>🛰️ NOVA ACCESS</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        pwd = st.text_input("QUANT-KEY", type="password")
        if st.button("LOGIN"):
            if pwd == "NOVA_ALPHA_2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("INVALID KEY")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ffffff/satellite.png", width=70)
    st.header("SYSTEM STATUS")
    st.success("🟢 CORE ONLINE")
    st.write("---")
    st.subheader("📡 LIVE GOES-16")
    st.image("https://services.swpc.noaa.gov/images/swx-overview-large.gif", use_container_width=True)

# --- DASHBOARD ---
st.title("🛰️ NOVA: Quantitative Terminal")
st.markdown("---")

# 1. METRIQUES (BLANC SUR NOIR)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Z-SCORE (SMH)", "2.68", "99% CONFIDENCE")
with c2: st.metric("WIN RATE", "37.5%", "+12% ALPHA")
with c3: st.metric("SHARPE", "0.35", "TAIL-RISK")
with c4: st.metric("SAMPLES", "200", "2000-2026")

# 2. GRAPH (Clarté des points)
if os.path.exists("master_massive_alpha.csv"):
    df = pd.read_csv("master_massive_alpha.csv")
    fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                     hover_data=['class'], color_continuous_scale='Viridis')
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# 3. NOVA INTELLIGENCE (TEXTE BLANC PUR)
st.write("---")
col_info_1, col_info_2 = st.columns([2, 1])

with col_info_1:
    st.subheader("📋 Historical Signal Log")
    st.dataframe(df.sort_values(by="vol_SMH", ascending=False).head(8), use_container_width=True)

with col_info_2:
    st.subheader("🧠 NOVA Intelligence")
    st.markdown("""
    <div style="background-color: #161b22; padding: 20px; border-left: 5px solid #58a6ff; border-radius: 5px;">
        <p style="color: #ffffff; font-weight: bold; margin-bottom: 5px;">STRATEGY INSIGHTS:</p>
        <ul style="color: #c9d1d9;">
            <li><b>SMH Sensitivity:</b> High-Beta detected during X-class spikes.</li>
            <li><b>VIX Correlation:</b> Primary systemic risk indicator confirmed.</li>
            <li><b>Timing:</b> 2-6h window for Gamma-hedging.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 4. SIMULATEUR (DANGER ZONE LISIBLE)
st.write("---")
st.subheader("🧪 Systemic Shock Simulator")

col_sim_1, col_sim_2 = st.columns([1, 2])

with col_sim_1:
    s_class = st.slider("Solar Magnitude (X-Class)", 1.0, 50.0, 10.0)
    exposure = st.number_input("Portfolio Exposure ($)", value=1000000)
    impact_pct = (s_class / 6.9) * 5.77
    var_loss = exposure * (impact_pct / 100)

with col_sim_2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = impact_pct,
        title = {'text': "Volatility Spike Projection (%)", 'font': {'color': 'white'}},
        gauge = {
            'axis': {'range': [0, 15], 'tickcolor': "white"},
            'bar': {'color': "#58a6ff"},
            'steps': [
                {'range': [0, 4], 'color': "#238636"},
                {'range': [4, 8], 'color': "#d29922"},
                {'range': [8, 15], 'color': "#f85149"}
            ]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# Alerte Finale (Rouge clair sur fond noir, texte blanc)
st.markdown(f"""
    <div style="background-color: #2a1215; border: 1px solid #f85149; padding: 15px; border-radius: 8px; text-align: center;">
        <h3 style="color: #f85149; margin: 0;">⚠️ RISK PROJECTION: X{s_class} FLARE</h3>
        <p style="color: white; font-size: 1.2rem; margin: 10px 0;">
            Projected Impact: <b>{impact_pct:.2f}%</b> | Estimated VaR: <b>${var_loss:,.0f}</b>
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("---")
st.caption("NOVA | Data: NASA/NOAA | Institutional Grade v2.5")
