import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuration
st.set_page_config(page_title="Score Flexible", layout="wide")

# 2. CSS optimisé
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    .joueur-header {
        text-align: center; font-size: 12px; font-weight: bold;
        color: #FF4B4B !important; margin-bottom: 2px;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .score-box {
        text-align: center; font-size: 22px; font-weight: 800;
        background-color: #262730; border-radius: 5px;
        padding: 4px 0px; margin-bottom: 5px; border: 1px solid #444;
    }
    div.stButton > button { height: 2.2em !important; padding: 0px !important; }
    /* Réduction de l'espace entre les colonnes */
    [data-testid="column"] { padding: 0px 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialisation
if 'scores' not in st.session_state:
    st.session_state.scores = {"J1": 0, "J2": 0, "J3": 0, "J4": 0, "J5": 0, "J6": 0}
if 'historique' not in st.session_state:
    st.session_state.historique = []

def enregistrer_action(joueur, points):
    if points == 0: return
    st.session_state.scores[joueur] += points
    temps = datetime.now().strftime("%H:%M")
    signe = "+" if points >= 0 else ""
    st.session_state.historique.insert(0, f"{temps} | {joueur} ({signe}{points})")
    st.session_state.historique = st.session_state.historique[:5]

def update_from_input(joueur):
    val = st.session_state[f"input_{joueur}"]
    if val != 0:
        enregistrer_action(joueur, val)
        st.session_state[f"input_{joueur}"] = 0

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # NOUVEAU : Réglage de la grille
    st.subheader("Affichage")
    cols_par_ligne = st.slider("Joueurs par ligne", 1, 8, 4)
    
    st.divider()
    noms_actuels = list(st.session_state.scores.keys())
    nb = st.number_input("Nombre total de joueurs", 1, 24, len(noms_actuels))
    
    nouveaux_scores = {}
    for i in range(nb):
        nom_par_defaut = noms_actuels[i] if i < len(noms_actuels) else f"J{i+1}"
        nouveau_nom = st.text_input(f"Joueur {i+1}", value=nom_par_defaut, key=f"edit_name_{i}")
        nouveaux_scores[nouveau_nom] = st.session_state.scores.get(nom_par_defaut, 0)

    if st.button("Appliquer les changements", use_container_width=True):
        st.session_state.scores = nouveaux_scores
        st.rerun()
    
    if st.button("🗑️ Reset Scores", use_container_width=True):
        for j in st.session_state.scores: st.session_state.scores[j] = 0
        st.session_state.historique = []
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏆 Scores")

# Grille dynamique
joueurs = list(st.session_state.scores.keys())
cols = st.columns(cols_par_ligne)

for index, joueur in enumerate(joueurs):
    # On place le joueur dans la colonne correspondante (boucle modulo)
    with cols[index % cols_par_ligne]:
        st.markdown(f'<p class="joueur-header">{joueur}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-box">{st.session_state.scores[joueur]}</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("＋", key=f"p_{joueur}", use_container_width=True):
            enregistrer_action(joueur, 1)
            st.rerun()
        if c2.button("－", key=f"m_{joueur}", use_container_width=True):
            enregistrer_action(joueur, -1)
            st.rerun()

        st.number_input(
            "Pts", value=0, step=1, key=f"input_{joueur}", 
            label_visibility="collapsed", on_change=update_from_input, args=(joueur,)
        )

st.divider()

# --- BAS DE PAGE ---
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
