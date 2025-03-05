import streamlit as st
from ui import afficher_liste_pokemon

st.set_page_config(
    page_title="Pokédex",
    page_icon="🔍",
    layout="wide"
)

st.title("Bienvenue dans le Pokédex !")

pages = st.sidebar.radio("Choisir une option", ["Liste des Pokémon"])

if pages == "Liste des Pokémon":
    afficher_liste_pokemon()
