# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search_games_with_cosine_similarity
import logging

app = Flask(__name__)
CORS(app)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return "Flask server is running! "


@app.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("query", "").strip()
        genre = request.args.get("genre", "").strip()
        platform = request.args.get("platform", "").strip()

        logger.info(f"Search request - Query: '{query}', Genre: '{genre}', Platform: '{platform}'")

        if not query:
            return jsonify({"error": "Search query cannot be empty"}), 400

        results = search_games_with_cosine_similarity(
            query=query,
            genre_filter=genre if genre else None,
            platform_filter=platform if platform else None
        )

        formatted_results = []
        for game in results:
            formatted_results.append({
                "name": game["name"],
                "description": game["description"],
                "genres": game["genres"],
                "platforms": game["platforms"],
                "image": game["image"],
                "score": game["score"]
            })

        logger.info(f"Returning {len(formatted_results)} results")
        return jsonify(formatted_results)

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({"error": "An error occurred during search"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
