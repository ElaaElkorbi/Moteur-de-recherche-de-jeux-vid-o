from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")

# fonction pour récupérer les jeux depuis Elasticsearch


def get_games_from_es():
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = es.search(index="games_index", body=query, size=100)
    games = []

    for hit in response["hits"]["hits"]:
        game = hit["_source"]
        games.append({
            "name": game["name"],
            "description": game["description"],
            "genres": game["genres"],
            "platforms": game["platforms"],
            "image": game["image"]
        })

    return games

# fonction pour rechercher des jeux avec la similarité Cosinus


def clean_query(query):
    generic_terms = {"game", "play", "fun", "cool", "nice", "title", 'a', 'an', 'the'}
    return " ".join([word for word in query.lower().split() if word not in generic_terms])


def search_games_with_cosine_similarity(query, genre_filter=None, platform_filter=None):
    games = get_games_from_es()

    # filtrage par genre et plateforme
    if genre_filter:
        games = [game for game in games if genre_filter.lower() in [g.lower() for g in game["genres"]]]

    if platform_filter:
        games = [game for game in games if platform_filter.lower() in [p.lower() for p in game["platforms"]]]

    if not games:
        return []

    # on combine description + nom + genres pour chaque jeu

    combined_texts = []
    for game in games:
        combined = f"{game['name']} {game['description']} {' '.join(game['genres'])}"
        combined_texts.append(combined)

    # calcul de la matrice TF-IDF

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(combined_texts)
    query_vector = vectorizer.transform([query])

    # similarité cosinus
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # préparer les résultats
    results = []
    for idx, game in enumerate(games):
        raw_score = float(cosine_similarities[idx])

        # ajustement de score
        capped_score = min(raw_score, 1)
        adjusted_score = capped_score * 100
        game_data = game.copy()
        game_data["score"] = adjusted_score
        results.append(game_data)

    # tri par pertinence
    results.sort(key=lambda x: x["score"], reverse=True)
    for i in results[:5]:
        print(i["score"])

    return results[:5]


# fonction pour effectuer la recherche avec l'entrée utilisateur


def user_search():
    query = ""
    genre_filter = ""
    genre_filter = genre_filter.strip() if genre_filter else None
    platform_filter = ""
    platform_filter = platform_filter.strip() if platform_filter else None

    # effectuer la recherche avec ou sans filtres de genre et de plateforme
    search_games_with_cosine_similarity(query, genre_filter, platform_filter)


user_search()
