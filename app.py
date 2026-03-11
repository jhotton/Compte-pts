import streamlit as st
import pandas as pd

# Configuration pour que l'app prenne toute la largeur
st.set_page_config(page_title="Score Master", page_icon="📱", layout="centered")

# CSS personnalisé pour agrandir les boutons sur mobile
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_config=True)

st.title("🏆 Score Master")

# --- PARAMÈTRES (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    nb_joueurs = st.number_input("Nombre de joueurs", 1, 20, 2)
    
    if 'scores' not in st.session_state or len(st.session_state.scores) != nb_joueurs:
        st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}

    if st.button("🔄 Remettre à zéro", use_container_width=True):
        st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
        st.rerun()

# --- INTERFACE DE JEU ---
st.subheader("Joueurs")

for joueur in st.session_state.scores.keys():
    # Un conteneur avec une bordure pour chaque joueur
    with st.container(border=True):
        col_name, col_score = st.columns([2, 1])
        with col_name:
            st.subheader(joueur)
        with col_score:
            st.write(f"### {st.session_state.scores[joueur]}")
        
        # Saisie des points simplifiée
        pts = st.number_input(f"Points à ajouter", step=1, key=f"in_{joueur}", label_visibility="collapsed")
        
        if st.button(f"Valider pour {joueur}", key=f"btn_{joueur}", use_container_width=True):
            st.session_state.scores[joueur] += pts
            st.rerun()

# --- CLASSEMENT & EXPORT ---
st.divider()
expander = st.expander("📊 Voir le classement & Exporter", expanded=False)

with expander:
    classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for i, (nom, sc) in enumerate(classement):
        st.write(f"{i+1}. **{nom}** : {sc} pts")
    
    df_scores = pd.DataFrame(list(st.session_state.scores.items()), columns=['Joueur', 'Score'])
    csv = df_scores.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger les scores", data=csv, file_name="scores.csv", use_container_width=True)
