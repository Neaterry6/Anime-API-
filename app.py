import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ API URLs
JIKAN_API = "https://api.jikan.moe/v4/anime?q="
KITSU_API = "https://kitsu.io/api/edge/anime?filter[text]="
ANILIST_API = "https://graphql.anilist.co"
SHIKIMORI_API = "https://shikimori.one/api/animes?search="
NYAA_SEARCH_URL = "https://nyaa.si/?f=0&c=1_2&q="  # ✅ Nyaa Torrent Search

@app.route("/search", methods=["GET"])
def search_anime():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide an anime name!"}), 400

    results = {}

    try:
        # ✅ Jikan API (MyAnimeList)
        response = requests.get(JIKAN_API + query)
        if response.status_code == 200:
            results["Jikan"] = response.json()

        # ✅ Kitsu API
        response = requests.get(KITSU_API + query)
        if response.status_code == 200:
            results["Kitsu"] = response.json()

        # ✅ AniList API (GraphQL Request)
        graphql_query = {"query": f"query {{ Media (search: \"{query}\") {{ title status episodes }} }}"}
        response = requests.post(ANILIST_API, json=graphql_query)
        if response.status_code == 200:
            results["AniList"] = response.json()

        # ✅ Shikimori API
        response = requests.get(SHIKIMORI_API + query)
        if response.status_code == 200:
            results["Shikimori"] = response.json()

        return jsonify(results)

    except Exception as e:
        print("Error:", str(e))  # ✅ Debugging
        return jsonify({"error": f"Server crashed: {str(e)}"}), 500

@app.route("/download", methods=["GET"])
def download_anime():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide an anime name!"}), 400

    try:
        search_url = NYAA_SEARCH_URL + query.replace(" ", "+")
        response = requests.get(search_url)

        print("Nyaa Search URL:", search_url)  # ✅ Debugging
        print("Nyaa Response Status Code:", response.status_code)  # ✅ Debugging

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # 🔥 Locate torrent rows properly
            torrents = soup.select("tr.default, tr.success")  # ✅ Ensuring correct torrent parsing
            download_links = []

            for torrent in torrents:
                try:
                    title_element = torrent.select_one("td a")
                    magnet_link_element = torrent.select_one("td a[href^='magnet']")

                    if title_element and magnet_link_element:
                        title = title_element.text.strip()
                        magnet_link = magnet_link_element["href"]

                        download_links.append({"title": title, "magnet_link": magnet_link})
                except Exception as err:
                    print(f"Error parsing torrent row: {err}")

            if download_links:
                return jsonify({"download_links": download_links})

        return jsonify({"error": "No torrents found for this anime!"})

    except Exception as e:
        print("Error:", str(e))  # ✅ Debugging
        return jsonify({"error": f"Server crashed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
