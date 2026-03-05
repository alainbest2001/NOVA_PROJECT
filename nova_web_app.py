import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import streamlit as st

# --- SYSTÈME D'ACCÈS PRIVÉ ---
def check_password():
    """Retourne True si l'utilisateur a saisi le bon mot de passe."""
    def password_entered():
        if st.session_state["password"] == "NOVA_ALPHA_2026": # Ton mot de passe ici
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # On ne garde pas le mdp en mémoire
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Affichage du formulaire de connexion
        st.markdown("<h1 style='text-align: center;'>🛰️ Terminal NOVA</h1>", unsafe_allow_html=True)
        st.text_input("Veuillez entrer le code d'accès institutionnel", 
                      type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state:
            st.error("❌ Code d'accès invalide.")
        st.stop() # Arrête le script ici si pas de mdp
        return False
    return True

if not check_password():
    st.stop()

# --- RESTE DE TON CODE (Dashboard, Graphiques, etc.) ---
st.success("🔓 Accès Autorisé : Session Quantifiée")




# Configuration de la page (Style Sombre/Quant)
st.set_page_config(page_title="NOVA | Space-Alpha Terminal", layout="wide", initial_sidebar_state="expanded")

# CSS Custom pour un look "Bloomberg Terminal"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🛰️ NOVA : Quantitative Space-Alpha")
st.subheader("Intervention sur les Risques Exogènes & Corrélation Solaire")
st.write("---")

# --- SIDEBAR (STATUS & FILTRES) ---
st.sidebar.image("https://img.icons8.com/fluency/96/000000/satellite.png", width=80)
st.sidebar.header("Système NOVA")
st.sidebar.success("🟢 Opérationnel : Satellite GOES-16")
st.sidebar.info("Flux : Rayons X (0.1-0.8 nm)")

# --- DASHBOARD DE PERFORMANCE ---
if os.path.exists("master_massive_alpha.csv"):
    df = pd.read_csv("master_massive_alpha.csv")
    
    # 1. KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Z-Score (SMH)", "2.68", "Significatif @ 99%")
    with col2: st.metric("Win Rate (X5+)", "37.5%", "+12% vs Random")
    with col3: st.metric("Sharpe Ratio", "0.35", "Tail-Risk Mode")
    with col4: st.metric("Events (N)", "200", "2000-2026")

    st.write("### 📈 Visualisation de l'Asymétrie de Risque")
    
    # 2. Graphique de Corrélation
    fig = px.scatter(df, x="date", y="vol_SMH", size="vol_VIX", color="vol_SMH",
                     hover_data=['class'], title="Dispersion de la Volatilité SMH par Événement Solaire",
                     color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 3. Répartition par classe
    col_left, col_right = st.columns(2)
    with col_left:
        st.write("### 📋 Distribution des Signaux")
        st.dataframe(df.sort_values(by="vol_SMH", ascending=False).head(10), use_container_width=True)
    
    with col_right:
        st.write("### 🧠 Intelligence Canonisée (DeepSeek-R1)")
        if os.path.exists("nova_multi_report.txt"):
            with open("nova_multi_report.txt", "r", encoding="utf-8") as f:
                st.info(f.read()[:800] + "...")
        else:
            st.warning("Générez d'abord le rapport avec nova_multi_expert.py")

else:
    st.error("Données manquantes. Lancez 'historic.py' pour générer le dataset.")

# --- FOOTER ---
st.write("---")
st.caption("NOVA Project | Data Source: NASA DONKI & NOAA SWPC | Compliance: CC0 Public Domain")

# --- SECTION : SIMULATEUR DE STRESS-TEST ---
st.write("---")
st.write("### 🧪 Simulateur de Choc Systémique (Stress-Test)")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.write("**Paramètres du Choc**")
    sim_class = st.slider("Intensité de l'éruption (Classe X)", 1.0, 50.0, 10.0)
    portfolio_value = st.number_input("Valeur de votre Portefeuille Tech ($)", value=1000000)
    
    # Calcul de l'impact basé sur le Z-Score et l'invariant 2011
    # Formule : (Classe / 6.9) * Vol_Moyenne_Historique
    impact_percent = (sim_class / 6.9) * 5.77
    impact_dollars = portfolio_value * (impact_percent / 100)

with col_sim2:
    st.write("**Projection de Risque NOVA**")
    
    # Jauge de risque visuelle
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = impact_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Volatilité Intra-day Estimée (%)"},
        gauge = {
            'axis': {'range': [None, 15]},
            'bar': {'color': "#ef4444"},
            'steps': [
                {'range': [0, 2], 'color': "#065f46"},
                {'range': [2, 5], 'color': "#92400e"},
                {'range': [5, 15], 'color': "#7f1d1d"}
            ],
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='#0e1117', font={'color': "white"}, height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- Résultat Narratif ---
st.error(f"""
    **ANALYSE DE SCÉNARIO :** Une éruption de classe **X{sim_class}** pourrait générer un pic de volatilité de 
    **{impact_percent:.2f}%**. Pour votre portefeuille, cela représente un risque d'exposition intra-day 
    de **{impact_dollars:,.0f} $**.
""")