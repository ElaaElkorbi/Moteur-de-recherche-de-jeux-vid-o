import requests
import json

API_KEY = "0ea50588a99743d9b375da91d6dd11e7"


def fetch_games_data(query, api_key, page=1, page_size=1):
    url = f"https://api.rawg.io/api/games?key={api_key}&search={query}&page={page}&page_size={page_size}&ordering=-user_game_count "
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["results"]
        games = []

        for game in data:
            game_id = game['id']
            game_details = requests.get(f"https://api.rawg.io/api/games/{game_id}?key={api_key}").json()
            description = game_details.get("description_raw", "Description non disponible")

            # ajout des données au tableau
            games.append({
                "name": game["name"],
                "description": description,
                "genres": [genre["name"] for genre in game.get("genres", [])],
                "platforms": [platform["platform"]["name"] for platform in game.get("platforms", [])],
                "image": game.get("background_image", "Image non disponible")
            })

        # enregistrer les données dans un fichier JSON
        with open("games_data.json", "a", encoding="utf-8") as file:
            json.dump(games, file, indent=4, ensure_ascii=False)

        print(f"{len(games)} jeux enregistrés avec succès !")
    else:
        print(f"Erreur lors de la récupération des données. Statut : {response.status_code}")


API_KEY = "0ea50588a99743d9b375da91d6dd11e7"
fetch_games_data("Fortnite", API_KEY)
