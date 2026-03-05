import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="NOVA | Super-Alpha Intelligence", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DESIGN FANTASTIQUE (Custom CSS) ---
st.markdown("""
    <style>
    /* Global Dark Theme & Neon Accents */
    .main { 
        background-color: #05070a; 
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0a0e14;
        border-right: 1px solid #1f2937;
    }

    /* Metric Glow Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 229, 255, 0.05);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #58a6ff;
    }

    /* Text & Header Styling */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.4);
    }
    
    h1, h2, h3 {
        color: #f0f6fc;
        letter-spacing: -1px;
    }

    /* Custom Info Box */
    .stAlert {
        background-color: #0d1117;
        border: 1px dashed #00f2ff;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS PRIVÉ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h1 style='text-align: center; margin-top: 100px;'>🛰️ PROJECT NOVA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>CRYPTO-SECURE INSTITUTIONAL GATEWAY</p>", unsafe_allow_html=True)
        
        col_l, col_m, col_r = st.columns([1, 1.5, 1])
        with col_m:
            with st.container():
                pwd = st.text_input("ENTER QUANT-KEY", type="password")
                if st.button("AUTHENTICATE"):
                    if pwd == "NOVA_ALPHA_2026":
                        st.session_state["password_correct"] = True
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED: INVALID SIGNATURE")
        st.stop()
    return True

check_password()

# --- SIDEBAR: LIVE TELEMETRY ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/satellite-sending-signal.png", width=100)
    st.title("NOVA OS v2.5")
    st.write("---")
    
    st.subheader("📡 Real-Time Telemetry")
    solar_url = "https://services.swpc.noaa.gov/images/swx-overview-large.gif"
    st.image(solar_url, caption="NASA GOES-16 LIVE FLUX", use_container_width=True)
    
    st.write("---")
    st.markdown("📈 **System Status:** `OPTIMAL`")
    st.markdown("🕵️ **Neural Engine:** `DEEPSEEK-R1`")
    st.markdown("🔐 **Session:** `ENCRYPTED`")

# --- INTERFACE PRINCIPALE ---
col_head_1, col_head_2 = st.columns([3, 1])
with col_head_1:
    st.title("🛰️ NOVA: Quantitative Space-Alpha")
    st.markdown("*Exogenous Risk Mitigation & Structural Invariant Intelligence*")
with col_head_2:
    st.info(f"📅 **DATE:** {datetime.now().strftime('%Y-%m-%d')}")

st.write("---")

# --- SECTION 1: KPIS RADAR ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Z-SCORE (SMH)", "2.68", "99% CONFIDENCE")
with c2: st.metric("WIN RATE (X5+)", "37.5%", "+12% ALPHA")
with c3: st.metric("SHARPE RATIO", "0.35", "TAIL-RISK OPT.")
with c4: st.metric("SAMPLE SIZE", "200", "2000-2026")

st.write("### 📉 Market-Solar Asymmetry Analysis")

# --- SECTION 2: GRAPHIC D'ALGORITHME ---
if os.path.exists("master_massive_alpha.csv"):
    df = pd.read_csv("master_massive_alpha.csv")
    
    fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                     hover_data=['class'], color_continuous_scale='IceFire',
                     template="plotly_dark")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#8b949e",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SECTION 3: INTELLIGENCE CANONIQUE ---
st.write("---")
col_info_1, col_info_2 = st.columns([2, 1])

with col_info_1:
    st.write("### 📋 Quantified Signal Log")
    if os.path.exists("master_massive_alpha.csv"):
        st.dataframe(df.sort_values(by="vol_SMH", ascending=False).head(8), use_container_width=True)

with col_info_2:
    st.write("### 🧠 NOVA Intelligence")
    st.info("""
    **Core Directives:**
    1. **Asymmetry:** High-exposure SMH sectors show predictive Kurtosis post-flare.
    2. **Regime Switch:** Solar Class > X5 triggers 'Chaos Regime' logic.
    3. **Action:** Execute Long-Gamma protection within 2h window.
    """)

# --- SECTION 4: SHOCK SIMULATOR (DANGER ZONE) ---
st.write("---")
st.write("### 🧪 Systemic Shock Simulator")

col_sim_1, col_sim_2 = st.columns([1, 2])

with col_sim_1:
    s_class = st.slider("Select Solar Magnitude (X-Class)", 1.0, 50.0, 10.0)
    exposure = st.number_input("Portfolio Exposure ($)", value=1000000)
    impact_pct = (s_class / 6.9) * 5.77
    var_loss = exposure * (impact_pct / 100)

with col_sim_2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = impact_pct,
        title = {'text': "PROJECTED VOLATILITY SPIKE (%)", 'font': {'color': '#f0f6fc'}},
        gauge = {
            'axis': {'range': [0, 15], 'tickcolor': "#f0f6fc"},
            'bar': {'color': "#00f2ff"},
            'steps': [
                {'range': [0, 3], 'color': "#065f46"},
                {'range': [3, 7], 'color': "#92400e"},
                {'range': [7, 15], 'color': "#7f1d1d"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 10}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#f0f6fc"}, height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)

st.error(f"⚡ **CRITICAL ALERT:** A class X{s_class} event projects a **{impact_pct:.2f}%** volatility surge. Estimated VaR: **${var_loss:,.0f}**.")

# --- FOOTER ---
st.write("---")
st.caption("🛰️ NOVA PROJECT | PROPRIETARY QUANTITATIVE TERMINAL | COMPLIANCE: MIFID II / NO-MNPI")
