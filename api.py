from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def get_accueil() -> str:
    return jsonify({
        "message": "Bienvenue dans l'API Pokémon!"
    })

# Route pour récupérer tous les Pokémon (sans pagination)
@app.route('/pokemon/list')
def get_all_pokemon():
    url = f"https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        count_pokemon = data['count']
        pokemon_name = [poke['name'] for poke in data['results']]
        return jsonify({
            'count': count_pokemon,
            'pokemon_liste': pokemon_name,
            'results': data['results']
        }), 200
    else:
        return jsonify({"error": "Unable to fetch Pokémon list"}), 500

# Route pour récupérer une liste de Pokémon avec pagination
@app.route('/pokemon/list/<int:page>/<int:items>', methods=['GET'])
def get_pokemon_list_paginated(page, items):
    offset = (page - 1) * items  
    url = f'https://pokeapi.co/api/v2/pokemon?limit={items}&offset={offset}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_names = [poke['name'] for poke in data['results']]
        return jsonify({
            "pokemon": pokemon_names,
            "total_count": data['count'],
            "current_page": page,
            "items_per_page": items
        }), 200
    return jsonify({"error": "Unable to fetch Pokémon list"}), 500

# Route pour récupérer un Pokémon spécifique par son nom
@app.route('/pokemon/<name>')
def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "image": data["sprites"]["front_default"]
        }), 200
    else:
        return jsonify({"error": "Pokémon non trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
