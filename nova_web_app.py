import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NOVA | Quantitative Space-Alpha Terminal", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- HIGH VISIBILITY CUSTOM CSS (Fix for dark mode metrics) ---
st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* Metrics High Visibility Fix */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important; /* Light grey for labels */
        font-size: 1.1rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981 !important; /* Emerald green for confidence/delta */
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PRIVATE ACCESS SYSTEM ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "NOVA_ALPHA_2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: white;'>🛰️ NOVA Terminal Access</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Please enter your institutional credentials to access Space-Alpha metrics.</p>", unsafe_allow_html=True)
        
        col_login_1, col_login_2, col_login_3 = st.columns([1, 2, 1])
        with col_login_2:
            st.text_input("Access Code", type="password", on_change=password_entered, key="password")
            if "password_correct" in st.session_state:
                st.error("❌ Access Denied: Invalid Credentials.")
        st.stop() 
        return False
    return True

if not check_password():
    st.stop()

# --- HEADER & TERMINAL STATUS ---
st.success("🔓 Access Granted: Secure Quantified Session Active")
st.title("🛰️ NOVA: Quantitative Space-Alpha")
st.subheader("Exogenous Risk Mitigation & Solar Correlation Engine")
st.write("---")

# --- SIDEBAR (SYSTEM STATUS) ---
st.sidebar.image("https://img.icons8.com/fluency/96/000000/satellite.png", width=80)
st.sidebar.header("NOVA Core Status")
st.sidebar.success("🟢 Online: GOES-16 Satellite")
st.sidebar.info("Flux: X-Ray (0.1-0.8 nm)")
st.sidebar.write("---")
st.sidebar.caption("Institutional Grade v2.4")

# --- PERFORMANCE DASHBOARD ---
if os.path.exists("master_massive_alpha.csv"):
    df = pd.read_csv("master_massive_alpha.csv")
    
    # 1. KPI Metrics (High Visibility)
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.metric("Z-Score (SMH)", "2.68", "Confidence: 99%")
    with col2: 
        st.metric("Win Rate (X5+)", "37.5%", "+12% vs Baseline")
    with col3: 
        st.metric("Sharpe Ratio", "0.35", "Tail-Risk Alpha")
    with col4: 
        st.metric("Sample Size (N)", "200", "Period: 2000-2026")

    st.write("### 📈 Risk Asymmetry Visualization")
    
    # 2. Interactive Correlation Plot
    fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                     hover_data=['class'], 
                     labels={"vol_SMH": "SMH Volatility (%)", "date": "Event Date"},
                     title="SMH Volatility Dispersion per Solar Event Severity",
                     color_continuous_scale='Viridis', template="plotly_dark")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 3. Data Distribution & Canonical Intelligence
    col_left, col_right = st.columns(2)
    with col_left:
        st.write("### 📋 Signal Distribution (Top 10 Events)")
        st.dataframe(df.sort_values(by="vol_SMH", ascending=False).head(10), use_container_width=True)
    
    with col_right:
        st.write("### 🧠 Canonical Intelligence (DeepSeek-R1)")
        st.info("""
            **Market Insights:**
            - **Asymmetry:** SMH (Semiconductors) exhibits significant over-reaction compared to XLU (Utilities) during X-class events.
            - **Indicator Priority:** The VIX acts as the primary systemic confirmation indicator for volatility spikes.
            - **Safe-Haven Lag:** Gold (GLD) remains a secondary lag-indicator, unsuitable for immediate intra-day hedging.
            - **Strategy Recommendation:** Volatility Arbitrage (Long Gamma) in 2-6 hour window post-flare.
        """)

else:
    st.error("Critical Data Missing. Please ensure 'master_massive_alpha.csv' is present in the repository.")

# --- STRESS-TEST SIMULATOR ---
st.write("---")
st.write("### 🧪 Systemic Shock Simulator (Stress-Test)")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.write("**Scenario Parameters**")
    sim_class = st.slider("Solar Flare Intensity (X-Class Rating)", 1.0, 50.0, 10.0)
    portfolio_value = st.number_input("Tech Portfolio Exposure ($)", value=1000000, step=100000)
    
    # Impact calculation based on 2011 Invariant
    impact_percent = (sim_class / 6.9) * 5.77
    impact_dollars = portfolio_value * (impact_percent / 100)

with col_sim2:
    st.write("**NOVA Risk Projection**")
    
    # Professional Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = impact_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Projected Intra-day Volatility (%)", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 15], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#ef4444"},
            'bgcolor': "#1f2937",
            'borderwidth': 2,
            'bordercolor': "#374151",
            'steps': [
                {'range': [0, 2], 'color': "#065f46"},
                {'range': [2, 5], 'color': "#92400e"},
                {'range': [5, 15], 'color': "#7f1d1d"}
            ],
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- Narrative Risk Outcome ---
st.error(f"""
    **SCENARIO ANALYSIS:** A class **X{sim_class}** event projects a **{impact_percent:.2f}%** volatility spike. 
    For your current exposure, this represents an estimated **Value at Risk (VaR)** of **${impact_dollars:,.0f}**.
""")

# --- FOOTER ---
st.write("---")
st.caption("NOVA Project | Data Source: NASA DONKI & NOAA SWPC | Compliance: CC0 Public Domain / No MNPI / MiFID II Compliant Signal")
