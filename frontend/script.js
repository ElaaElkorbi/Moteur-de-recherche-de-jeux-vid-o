document.getElementById("search-btn").addEventListener("click", searchGames);
document
  .getElementById("toggleGenres")
  .addEventListener("click", () => toggleOption("genres"));
document
  .getElementById("toggleImage")
  .addEventListener("click", () => toggleOption("image"));
document
  .getElementById("togglePlatforms")
  .addEventListener("click", () => toggleOption("platforms"));

let options = {
  genres: false,
  image: false,
  platforms: false,
};

function toggleOption(option) {
  options[option] = !options[option];
  searchGames();
}

function searchGames() {
  const query = document.getElementById("search-input").value;

  if (!query) {
    alert("Veuillez entrer une description !");
    return;
  }

  fetch(`http://localhost:5000/search?query=${encodeURIComponent(query)}`)
    .then((response) => response.json())
    .then((data) => displayResults(data))
    .catch((error) => console.error("Erreur lors de la recherche :", error));
}

function displayResults(games) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  if (games.length === 0) {
    resultsDiv.innerHTML = "<p>Aucun jeu trouvé.</p>";
    return;
  }

  const maxScore = Math.max(...games.map((game) => game.score || 1), 1);

  games.forEach((game) => {
    let gameDiv = document.createElement("div");
    gameDiv.classList.add("game");

    let content = `<h2>${game.name}</h2>`;

    if (options.genres) {
      content += `<p><i class="fas fa-layer-group"></i> <strong>Genres :</strong> ${game.genres.join(
        ", "
      )}</p>`;
    }
    if (options.platforms) {
      content += `<p><i class="fas fa-laptop"></i> <strong>Plateformes :</strong> ${game.platforms.join(
        ", "
      )}</p>`;
    }
    if (options.image) {
      content += `<img src="https://images.weserv.nl/?url=${game.image}" alt="${game.name}">`;
    }

    const percentage = game.score.toFixed(0);

    content += `
      <div class="progress-container">
        <div class="progress-label">Pertinence: ${percentage}%</div>
        <div class="progress-bar">
          <div class="progress" style="width: ${percentage}%;"></div>
        </div>
      </div>
    `;
    if (percentage != 0) {
      gameDiv.innerHTML = content;
      resultsDiv.appendChild(gameDiv);
    } else {
      resultsDiv.innerHTML = "no games found ! try again";
    }
  });
}
