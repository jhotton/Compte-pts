import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuration (Toujours en haut)
st.set_page_config(page_title="Score Ultra-Fast", layout="wide")

# 2. CSS pour stabiliser l'affichage
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    .joueur-header {
        text-align: center; font-size: 13px; font-weight: bold;
        color: #FF4B4B !important; margin-bottom: 2px;
    }
    .score-box {
        text-align: center; font-size: 24px; font-weight: 800;
        background-color: #262730; border-radius: 5px;
        padding: 5px 0px; margin-bottom: 5px; border: 1px solid #444;
    }
    div.stButton > button { height: 2.5em !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialisation des données
if 'scores' not in st.session_state:
    st.session_state.scores = {"J1": 0, "J2": 0, "J3": 0, "J4": 0}
if 'historique' not in st.session_state:
    st.session_state.historique = []

def enregistrer_action(joueur, points):
    temps = datetime.now().strftime("%H:%M")
    signe = "+" if points >= 0 else ""
    st.session_state.historique.insert(0, f"{temps} | {joueur} ({signe}{points})")
    st.session_state.historique = st.session_state.historique[:5]

# 4. Le Fragment : La magie est ici
@st.fragment
def grille_de_score():
    cols = st.columns(4)
    joueurs = list(st.session_state.scores.keys())
    
    for index, joueur in enumerate(joueurs):
        with cols[index % 4]:
            st.markdown(f'<p class="joueur-header">{joueur}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="score-box">{st.session_state.scores[joueur]}</div>', unsafe_allow_html=True)
            
            # Boutons rapides
            c1, c2 = st.columns(2)
            if c1.button("＋", key=f"p_{joueur}", use_container_width=True):
                st.session_state.scores[joueur] += 1
                enregistrer_action(joueur, 1)
                st.rerun(scope="fragment") # Relance uniquement cette fonction
            
            if c2.button("－", key=f"m_{joueur}", use_container_width=True):
                st.session_state.scores[joueur] -= 1
                enregistrer_action(joueur, -1)
                st.rerun(scope="fragment")

            # Saisie libre
            val = st.number_input("Pts", step=1, key=f"v_{joueur}", label_visibility="collapsed")
            if st.button("OK", key=f"ok_{joueur}", use_container_width=True):
                st.session_state.scores[joueur] += val
                enregistrer_action(joueur, val)
                st.rerun(scope="fragment")

# --- AFFICHAGE PRINCIPAL ---

st.title("🏆 Scores")

# Appel du fragment
grille_de_score()

st.divider()

# Section Historique et Classement (se mettront à jour au prochain refresh global ou manuel)
col_h, col_c = st.columns(2)
with col_h:
    st.caption("🕒 Historique (5 derniers)")
    for item in st.session_state.historique:
        st.write(item)

with col_c:
    with st.expander("🏆 Classement complet"):
        classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        for i, (n, s) in enumerate(classement):
            st.write(f"**{n}**: {s}")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Configuration")
    if st.button("🔄 Refresh global / Classement"):
        st.rerun()
    
    st.divider()
    nb = st.number_input("Nombre de joueurs", 1, 20, len(st.session_state.scores))
    if st.button("Réinitialiser avec ce nombre"):
        st.session_state.scores = {f"J{i+1}": 0 for i in range(nb)}
        st.session_state.historique = []
        st.rerun()
