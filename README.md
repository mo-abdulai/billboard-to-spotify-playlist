# Billboard Top 100 Playlist to Spotify

This script allows you to create a Spotify playlist with the top 100 songs from Billboard's Hot 100 chart for a specific date. The playlist will be generated on your Spotify account using the Spotipy library.

## Prerequisites

Before you can run this script, you need to have the following:

1. **Python**: Ensure you have Python installed on your machine.
2. **Spotify Developer Account**: Create a Spotify developer account and set up an application to get your `CLIENT_ID` and `CLIENT_SECRET`.
3. **Spotipy Library**: Install the Spotipy library to interact with the Spotify API.
4. **Requests Library**: To make HTTP requests.
5. **BeautifulSoup Library**: For web scraping the Billboard website.
6. **Dotenv Library**: To manage environment variables securely.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/billboard-spotify-playlist.git
    cd billboard-spotify-playlist
    ```

2. Install the required libraries:

    ```bash
    pip install spotipy requests beautifulsoup4 python-dotenv
    ```

3. Create a `.env` file in the project root directory and add your Spotify API credentials:

    ```env
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    ```

## Usage

1. Run the script:

    ```bash
    python script_name.py
    ```

2. When prompted, enter the date for which you want to retrieve the Billboard Hot 100 chart in the format `YYYY-MM-DD`.

3. Authenticate with your Spotify account. A browser window will open for you to log in and authorize the application.

4. The script will create a private playlist on your Spotify account with the top 100 songs from the specified date.

## Code Explanation

1. **Importing Libraries**: The script imports the necessary libraries for web scraping, HTTP requests, and Spotify API interactions.
   
    ```python
    from bs4 import BeautifulSoup
    import requests
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import os
    from dotenv import load_dotenv
    ```

2. **Load Environment Variables**: It loads the Spotify API credentials from the `.env` file.

    ```python
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    ```

3. **User Input**: The script prompts the user to enter a date.

    ```python
    user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
    ```

4. **Web Scraping**: It fetches the Billboard Hot 100 chart for the specified date using BeautifulSoup.

    ```python
    URL = f"https://www.billboard.com/charts/hot-100/{user_date}/"
    response = requests.get(URL)
    website_html = response.text
    soup = BeautifulSoup(website_html, "html.parser")
    all_song = soup.select("li ul li h3")
    song_title = [song.getText().strip() for song in all_song]
    ```

5. **Spotify Authentication**: The script authenticates with the Spotify API using the Spotipy library.

    ```python
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://localhost:4304/auth/spotify/callback",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True,
            cache_path="token.txt",
            username="your_spotify_username",
        )
    )
    user_id = sp.current_user()["id"]
    ```

6. **Song Search and Playlist Creation**: It searches for each song on Spotify and adds them to a new playlist.

    ```python
    song_uris = []
    year = user_date.split("-")[0]
    for song in song_title:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    ```

## Notes

- Ensure your Spotify app has the appropriate redirect URI set in the Spotify Developer Dashboard.
- The script currently handles cases where songs are not found on Spotify by skipping them and printing a message.


---

Feel free to contribute to this project by submitting issues or pull requests. Happy playlist creating!
