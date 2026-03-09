import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Compteur de Points", page_icon="🏆")

st.title("🏆 Compteur de Points")

# 1. Configuration dans la barre latérale
with st.sidebar:
    st.header("Paramètres")
    nb_joueurs = st.number_input("Nombre de joueurs", min_value=1, max_value=20, value=2)
            
                # Initialisation ou mise à jour du nombre de joueurs
                    if 'scores' not in st.session_state or len(st.session_state.scores) != nb_joueurs:
                            st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}

                                if st.button("Réinitialiser tous les scores"):
                                        st.session_state.scores = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
                                                st.rerun()

                                                # 2. Zone d'affichage et de saisie
                                                st.subheader("Tableau des scores")
                                                cols = st.columns(2)

                                                for index, (joueur, score) in enumerate(st.session_state.scores.items()):
                                                    with cols[index % 2]:
                                                            st.write(f"### {joueur}")
                                                                    st.metric(label="Total", value=score)
                                                                            
                                                                                    # Saisie de points (positifs ou négatifs)
                                                                                            points = st.number_input(f"Points pour {joueur}", value=0, key=f"in_{joueur}")
                                                                                                    
                                                                                                            if st.button(f"Ajouter", key=f"btn_{joueur}"):
                                                                                                                        st.session_state.scores[joueur] += points
                                                                                                                                    st.rerun()

                                                                                                                                    # 3. Classement et Exportation
                                                                                                                                    st.divider()
                                                                                                                                    col_left, col_right = st.columns([2, 1])

                                                                                                                                    with col_left:
                                                                                                                                        st.subheader("📊 Classement")
                                                                                                                                            classement = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
                                                                                                                                                for i, (nom, sc) in enumerate(classement):
                                                                                                                                                        st.write(f"{i+1}. **{nom}** : {sc} pts")

                                                                                                                                                        with col_right:
                                                                                                                                                            st.subheader("💾 Sauvegarder")
                                                                                                                                                                # Création du CSV
                                                                                                                                                                    df_scores = pd.DataFrame(list(st.session_state.scores.items()), columns=['Joueur', 'Score'])
                                                                                                                                                                        csv = df_scores.to_csv(index=False).encode('utf-8')
                                                                                                                                                                            
                                                                                                                                                                                st.download_button(
                                                                                                                                                                                        label="Télécharger CSV",
                                                                                                                                                                                                data=csv,
                                                                                                                                                                                                        file_name="resultats_partie.csv",
                                                                                                                                                                                                                mime="text/csv",
                                                                                                                                                                                                                    )