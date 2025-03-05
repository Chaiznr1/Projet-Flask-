import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

# Fonction pour afficher la liste paginée des Pokémon
def afficher_liste_pokemon():
    st.title("Liste des Pokémon")

    # Demander à l'utilisateur de choisir la page et le nombre d'éléments par page
    page = st.number_input("Page", min_value=1, value=1)
    items_per_page = st.selectbox("Nombre d'éléments par page", [10, 25, 50], index=0)

    # Requête à l'API Flask pour récupérer la liste paginée des Pokémon
    response = requests.get(f'{API_URL}/pokemon/list/{page}/{items_per_page}')
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_names = pokemon_data["pokemon"]
        
        # Afficher les Pokémon de la page actuelle
        st.write(f"Page {pokemon_data['current_page']} / Total de Pokémon: {pokemon_data['total_count']}")
        st.write(f"Affichage de {len(pokemon_names)} Pokémon sur {pokemon_data['items_per_page']} par page.")

        # Permettre à l'utilisateur de choisir un Pokémon dans la liste
        selected_pokemon = st.selectbox("Choisissez un Pokémon", pokemon_names)
        
        # Afficher les détails du Pokémon sélectionné
        if selected_pokemon:
            afficher_details_pokemon(selected_pokemon)
        
        # Navigation entre les pages
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if page > 1:
                if st.button("Page Précédente"):
                    afficher_liste_pokemon(page=page-1, items_per_page=items_per_page)
        with col3:
            if len(pokemon_names) == items_per_page:  
                if st.button("Page Suivante"):
                    afficher_liste_pokemon(page=page+1, items_per_page=items_per_page)
                
    else:
        st.error("Erreur lors de la récupération des Pokémon")

# Fonction pour afficher les détails d'un Pokémon
def afficher_details_pokemon(pokemon_name):
    response = requests.get(f'{API_URL}/pokemon/{pokemon_name}')
    if response.status_code == 200:
        pokemon_data = response.json()
        st.subheader(pokemon_data['name'])
        st.image(pokemon_data['image'], caption=f"Image de {pokemon_data['name']}")
        st.write(f"Taille: {pokemon_data['height']} m")
        st.write(f"Poids: {pokemon_data['weight']} kg")
        st.write(f"Types: {', '.join(pokemon_data['types'])}")
    else:
        st.error("Impossible de récupérer les détails du Pokémon")

afficher_liste_pokemon()
