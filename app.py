import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuration
st.set_page_config(page_title="Score Live", layout="wide")

# 2. CSS (Visibilité et format compact)
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    .joueur-header {
        text-align: center; font-size: 13px; font-weight: bold;
        color: #FF4B4B !important; margin-bottom: 2px;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .score-box {
        text-align: center; font-size: 24px; font-weight: 800;
        background-color: #262730; border-radius: 5px;
        padding: 5px 0px; margin-bottom: 5px; border: 1px solid #444;
    }
    div.stButton > button { height: 2.2em !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialisation de l'état
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
    val = st.session_state[f"input_{joueur}"]
    if val != 0:
        enregistrer_action(joueur, val)
        st.session_state[f"input_{joueur}"] = 0

# --- BARRE LATÉRALE (GESTION DES NOMS) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Étape A : Nombre de joueurs
    noms_actuels = list(st.session_state.scores.keys())
    nb = st.number_input("Nombre de joueurs", 1, 20, len(noms_actuels))
    
    # Étape B : Saisie des noms
    nouveaux_scores = {}
    st.write("---")
    st.subheader("Noms des joueurs")
    for i in range(nb):
        # On essaie de récupérer le nom existant, sinon on crée "J+1"
        nom_par_defaut = noms_actuels[i] if i < len(noms_actuels) else f"J{i+1}"
        nouveau_nom = st.text_input(f"Joueur {i+1}", value=nom_par_defaut, key=f"edit_name_{i}")
        
        # On transfère le score de l'ancien nom vers le nouveau
        score_existant = st.session_state.scores.get(nom_par_defaut, 0)
        nouveaux_scores[nouveau_nom] = score_existant

    # Étape C : Application des changements
    if st.button("Valider les noms/nombre", use_container_width=True):
        st.session_state.scores = nouveaux_scores
        st.rerun()
    
    st.write("---")
    if st.button("🗑️ Reset Scores & Historique", use_container_width=True):
        for j in st.session_state.scores: st.session_state.scores[j] = 0
        st.session_state.historique = []
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏆 Scores")

# Grille de score (4 colonnes)
cols = st.columns(4)
joueurs = list(st.session_state.scores.keys())

for index, joueur in enumerate(joueurs):
    with cols[index % 4]:
        st.markdown(f'<p class="joueur-header">{joueur}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-box">{st.session_state.scores[joueur]}</div>', unsafe_allow_html=True)
        
        # Boutons rapides
        c1, c2 = st.columns(2)
        if c1.button("＋", key=f"p_{joueur}", use_container_width=True):
            enregistrer_action(joueur, 1)
            st.rerun()
        if c2.button("－", key=f"m_{joueur}", use_container_width=True):
            enregistrer_action(joueur, -1)
            st.rerun()

        # Saisie directe
        st.number_input(
            "Pts", value=0, step=1, key=f"input_{joueur}", 
            label_visibility="collapsed", on_change=update_from_input, args=(joueur,)
        )

st.divider()

# --- HISTORIQUE & CLASSEMENT ---
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
