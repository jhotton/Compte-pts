import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuration
st.set_page_config(page_title="Score Live", layout="wide")

# 2. CSS (Maintien de la visibilité et du format compact)
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
    div.stButton > button { height: 2.2em !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialisation
if 'scores' not in st.session_state:
    st.session_state.scores = {"J1": 0, "J2": 0, "J3": 0, "J4": 0}
if 'historique' not in st.session_state:
    st.session_state.historique = []

# 4. Fonctions de mise à jour
def enregistrer_action(joueur, points):
    if points == 0: return
    st.session_state.scores[joueur] += points
    temps = datetime.now().strftime("%H:%M")
    signe = "+" if points >= 0 else ""
    st.session_state.historique.insert(0, f"{temps} | {joueur} ({signe}{points})")
    st.session_state.historique = st.session_state.historique[:5]

def update_from_input(joueur):
    # Récupérer la valeur saisie via sa clé unique
    val = st.session_state[f"input_{joueur}"]
    if val != 0:
        enregistrer_action(joueur, val)
        # On remet le champ de saisie à 0 après validation
        st.session_state[f"input_{joueur}"] = 0

# --- INTERFACE PRINCIPALE ---
st.title("🏆 Scores en Direct")

# Grille de score
cols = st.columns(4)
joueurs = list(st.session_state.scores.keys())

for index, joueur in enumerate(joueurs):
    with cols[index % 4]:
        st.markdown(f'<p class="joueur-header">{joueur}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-box">{st.session_state.scores[joueur]}</div>', unsafe_allow_html=True)
        
        # Boutons rapides +1 / -1
        c1, c2 = st.columns(2)
        if c1.button("＋", key=f"p_{joueur}", use_container_width=True):
            enregistrer_action(joueur, 1)
            st.rerun()
        if c2.button("－", key=f"m_{joueur}", use_container_width=True):
            enregistrer_action(joueur, -1)
            st.rerun()

        # Saisie directe (se valide dès qu'on appuie sur Entrée ou qu'on change de champ)
        st.number_input(
            "Pts", 
            value=0, 
            step=1, 
            key=f"input_{joueur}", 
            label_visibility="collapsed",
            on_change=update_from_input, 
            args=(joueur,)
        )

st.divider()

# --- HISTORIQUE & CLASSEMENT (Mise à jour instantanée) ---
col_h, col_c = st.columns(2)
with col_h:
    st.subheader("🕒 Historique")
    for item in st.session_state.historique:
        st.write(item)

with col_c:
    st.subheader("📊 Classement")
    classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for i, (n, s) in enumerate(classement):
        st.write(f"**{i+1}. {n}** : {s} pts")

# Barre latérale pour la gestion
with st.sidebar:
    st.header("⚙️ Configuration")
    if st.button("🔄 Réinitialiser la partie", use_container_width=True):
        st.session_state.scores = {joueur: 0 for joueur in st.session_state.scores}
        st.session_state.historique = []
        st.rerun()
