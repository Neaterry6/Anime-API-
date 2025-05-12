import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

ANIAPI_URL = "https://api.aniapi.com/v1/anime"
NYAA_SEARCH_URL = "https://nyaa.si/?f=0&c=1_2&q="  # ✅ Nyaa Torrent Search

@app.route("/search", methods=["GET"])
def search_anime():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide an anime name!"}), 400

    params = {"title": query}
    response = requests.get(ANIAPI_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)

    return jsonify({"error": "Anime not found!"})

@app.route("/download", methods=["GET"])
def download_anime():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide an anime name!"}), 400

    search_url = NYAA_SEARCH_URL + query.replace(" ", "+")
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        torrents = soup.find_all("a", href=True)
        download_links = [link["href"] for link in torrents if "magnet" in link["href"]]
        
        if download_links:
            return jsonify({"download_links": download_links})

    return jsonify({"error": "No torrents found for this anime!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
