from elasticsearch import Elasticsearch
import json

# connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")

# création de l'index (s'il n'existe pas déjà)

index_name = "games_index"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# chargement des données

with open("games_data.json", "r", encoding="utf-8") as file:
    games = json.load(file)

# indexation des données
for idx, game in enumerate(games):
    es.index(index=index_name, id=idx + 1, document=game)

print(f"{len(games)} jeux indexés avec succès dans Elasticsearch !")
