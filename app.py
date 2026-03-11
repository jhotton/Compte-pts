import streamlit as st
import pandas as pd

st.set_page_config(page_title="Score Mini", layout="wide")

# CSS pour compacter au maximum
st.markdown("""
    <style>
    /* Supprimer les marges inutiles */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    /* Style des boutons compacts */
    div.stButton > button {
        padding: 0px;
        height: 2em !important;
        font-size: 14px !important;
    }
    
    /* Style des entrées numériques compactes */
    div[data-testid="stNumberInput"] {
        margin-bottom: -15px;
    }
    
    /* Centrer le texte */
    .joueur-name {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 0px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .joueur-score {
        text-align: center;
        font-size: 20px;
        color: #FF4B4B;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation
if 'scores' not in st.session_state:
    st.session_state.scores = {f"J{i+1}": 0 for i in range(4)}

# --- BARRE LATERALE ---
with st.sidebar:
    nb = st.number_input("Joueurs", 1, 20, len(st.session_state.scores))
    if st.button("Appliquer/Reset"):
        st.session_state.scores = {f"J{i+1}": 0 for i in range(nb)}
        st.rerun()

# --- GRILLE DE JEU ---
# On crée 4 colonnes
cols = st.columns(4)

for index, (joueur, score) in enumerate(st.session_state.scores.items()):
    with cols[index % 4]:
        # Affichage Nom et Score
        st.markdown(f'<p class="joueur-name">{joueur}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="joueur-score">{score}</p>', unsafe_allow_html=True)
        
        # Saisie très courte (on utilise step=1 pour avoir les boutons +/-)
        val = st.number_input("+/-", value=1, step=1, key=f"v_{joueur}", label_visibility="collapsed")
        
        # Bouton de validation compact
        if st.button("OK", key=f"b_{joueur}", use_container_width=True):
            st.session_state.scores[joueur] += val
            st.rerun()

st.divider()

# --- CLASSEMENT DISCRET ---
with st.expander("Classement"):
    for j, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{j}**: {s}")
