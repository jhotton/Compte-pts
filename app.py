import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(
    page_title="Score Master", 
    page_icon="📱", 
    layout="centered"
)

# 2. CSS pour l'ergonomie mobile (boutons plus grands et tactiles)
st.markdown("""
    <style>
    /* Agrandir les boutons pour les pouces */
    div.stButton > button:first-child {
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    /* Style pour les cartes de joueurs */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #f9f9f9;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Score Master")

# 3. Barre latérale (Paramètres)
with st.sidebar:
    st.header("⚙️ Configuration")
    nb_joueurs = st.number_input("Nombre de joueurs", min_value=1, max_value=20, value=2)
    
    # Initialisation de l'état des scores
    if 'scores' not in st.session_state or len(st.session_state.scores) != nb_joueurs:
        st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}

    if st.button("🔄 Reset Global", use_container_width=True):
        st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
        st.rerun()

# 4. Interface de saisie des points
st.subheader("Tableau de marque")

for joueur in list(st.session_state.scores.keys()):
    # Utilisation d'un conteneur avec bordure pour l'aspect "carte" mobile
    with st.container(border=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"### {joueur}")
        with c2:
            st.markdown(f"## {st.session_state.scores[joueur]}")
        
        # Champ de saisie (type "number" pour clavier numérique sur mobile)
        points = st.number_input(
            f"Points pour {joueur}", 
            step=1, 
            key=f"input_{joueur}", 
            label_visibility="collapsed"
        )
        
        if st.button(f"Ajouter à {joueur}", key=f"btn_{joueur}", use_container_width=True):
            st.session_state.scores[joueur] += points
            st.rerun()

# 5. Classement et Exportation
st.divider()
with st.expander("📊 Classement final & Export", expanded=False):
    classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (nom, sc) in enumerate(classement):
        medaille = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "👤"
        st.write(f"{medaille} **{nom}** : {sc} pts")
    
    st.divider()
    
    # Préparation du fichier CSV
    df_scores = pd.DataFrame(list(st.session_state.scores.items()), columns=['Joueur', 'Score'])
    csv = df_scores.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Télécharger le CSV",
        data=csv,
        file_name="scores_partie.csv",
        mime="text/csv",
        use_container_width=True
    )
