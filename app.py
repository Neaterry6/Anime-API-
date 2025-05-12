import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Use FreeWebAPI instead of AniAPI
FREEWEBAPI_ANIME_URL = "https://freewebapi.com/api/anime/search"
NYAA_SEARCH_URL = "https://nyaa.si/?f=0&c=1_2&q="  # ✅ Nyaa Torrent Search

@app.route("/search", methods=["GET"])
def search_anime():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide an anime name!"}), 400

    try:
        params = {"query": query}
        response = requests.get(FREEWEBAPI_ANIME_URL, params=params)

        print("API Response Status Code:", response.status_code)  # ✅ Debugging
        print("API Response Body:", response.text)  # ✅ Debugging

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)

        return jsonify({"error": f"Anime not found! API returned {response.status_code}"})

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
