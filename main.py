from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")

URL = f"https://www.billboard.com/charts/hot-100/{user_date}/"
response = requests.get(URL)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:4304/auth/spotify/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Mohammed Abdulai",
    )
)

user_id = sp.current_user()["id"]

website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

all_song = soup.select("li ul li h3")
song_title = [song.getText().strip() for song in all_song]

song_uris = []
year = user_date.split("-")[0]
for song in song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)