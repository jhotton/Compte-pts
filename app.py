import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Score Express+", layout="wide")

# --- CSS CORRECTIF (Fix pour le texte tronqué et le mode sombre) ---
st.markdown("""
    <style>
    /* Ajout d'un espace en haut pour ne pas tronquer les noms */
    .block-container { 
        padding-top: 2rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
    }
    
    /* Style du nom du joueur avec couleur forcée */
    .joueur-header {
        text-align: center; 
        font-size: 14px; 
        font-weight: bold;
        text-transform: uppercase; 
        color: #FF4B4B !important; /* Couleur rouge Streamlit pour être visible partout */
        margin-bottom: 5px;
        display: block;
    }
    
    /* Affichage du score */
    .score-box {
        text-align: center; 
        font-size: 24px; 
        font-weight: 800;
        color: #FFFFFF !important; 
        background-color: #262730; /* Fond gris foncé pour contraste */
        border: 1px solid #444;
        border-radius: 5px; 
        padding: 5px 0px; 
        margin-bottom: 8px;
    }

    /* Taille des boutons */
    div.stButton > button {
        height: 2.5em !important; 
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'scores' not in st.session_state:
    st.session_state.scores = {"J1": 0, "J2": 0, "J3": 0, "J4": 0}
if 'historique' not in st.session_state:
    st.session_state.historique = []

def ajouter_points(joueur, points):
    st.session_state.scores[joueur] += points
    temps = datetime.now().strftime("%H:%M")
    signe = "+" if points >= 0 else ""
    st.session_state.historique.insert(0, f"{temps} | {joueur} ({signe}{points})")
    st.session_state.historique = st.session_state.historique[:5]

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    noms_actuels = list(st.session_state.scores.keys())
    nb_joueurs = st.number_input("Nombre de joueurs", 1, 20, len(noms_actuels))
    
    new_scores = {}
    for i in range(nb_joueurs):
        nom_defaut = noms_actuels[i] if i < len(noms_actuels) else f"J{i+1}"
        nom = st.text_input(f"Nom {i+1}", value=nom_defaut, key=f"name_{i}")
        new_scores[nom] = st.session_state.scores.get(nom, 0)
    
    if st.button("Mettre à jour / Reset"):
        st.session_state.scores = new_scores
        st.session_state.historique = []
        st.rerun()

# --- GRILLE DE SCORE (4 colonnes) ---
st.title("🏆 Scores")
cols = st.columns(4)
joueurs_items = list(st.session_state.scores.items())

for index, (joueur, score) in enumerate(joueurs_items):
    with cols[index % 4]:
        # On utilise un conteneur pour grouper proprement
        st.markdown(f'<span class="joueur-header">{joueur}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-box">{score}</div>', unsafe_allow_html=True)
        
        c_plus, c_moins = st.columns(2)
        with c_plus:
            if st.button("＋", key=f"p_{joueur}", use_container_width=True):
                ajouter_points(joueur, 1)
                st.rerun()
        with c_moins:
            if st.button("－", key=f"m_{joueur}", use_container_width=True):
                ajouter_points(joueur, -1)
                st.rerun()
        
        val = st.number_input("Pts", step=1, key=f"v_{joueur}", label_visibility="collapsed")
        if st.button("OK", key=f"ok_{joueur}", use_container_width=True):
            if val != 0:
                ajouter_points(joueur, val)
                st.rerun()

st.divider()

# --- SECTION BAS DE PAGE ---
col_h, col_c = st.columns([1, 1])
with col_h:
    st.caption("🕒 Historique")
    for item in st.session_state.historique:
        st.write(item)

with col_c:
    with st.expander("🏆 Classement"):
        classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        for i, (n, s) in enumerate(classement):
            st.write(f"**{n}**: {s}")
