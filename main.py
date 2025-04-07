# spotify_playlist_generator.py

from datetime import datetime, timedelta
from typing import List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time
import socket

load_dotenv()

# ----- CONFIG -----
CONFIG = {
    "artists": ["Drake"],
    # Make the playlist name dynamic, based on the current date
    "playlist_id": f"New tracks for the week of {datetime.now().strftime('%m/%d/%Y')}",
    "days_back": 100,
    "vibe_filter": {
        "min_energy": 0.6,
        "min_danceability": 0.6,
        "max_acousticness": 0.4,
    },
}

# Global variable to store the auth code
auth_code = None
port = 8888

def find_available_port(start_port):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        # Extract the code from the URL
        if 'code=' in self.path:
            auth_code = self.path.split('code=')[1].split('&')[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authentication successful! You can close this window.')
            # Stop the server
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        # Suppress logging
        return

def start_local_server():
    global port
    port = find_available_port(8888)
    server = HTTPServer(('localhost', port), OAuthHandler)
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server

# ----- SPOTIFY CLIENT -----
def get_spotify_client() -> spotipy.Spotify:
    # Start local server
    server = start_local_server()
    
    # Create OAuth manager
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=f"http://localhost:{port}",
        scope="playlist-modify-public playlist-modify-private user-read-private",
        cache_path=".cache"
    )
    
    # Get auth URL and open in browser
    auth_url = auth_manager.get_authorize_url()
    print(f"Please authorize the application by visiting: {auth_url}")
    webbrowser.open(auth_url)
    
    # Wait for the auth code
    while auth_code is None:
        time.sleep(1)
    
    # Get the token
    token = auth_manager.get_access_token(auth_code)
    
    # Create and return the Spotify client
    return spotipy.Spotify(auth_manager=auth_manager)


# ----- TRACK DISCOVERY MODULE -----
def get_new_tracks(
    sp: spotipy.Spotify, artist_names: List[str], since_days: int
) -> List[str]:
    new_track_ids = []
    date_cutoff = (datetime.now() - timedelta(days=since_days)).date().isoformat()

    # Get all albums from all artists
    for artist_name in artist_names:
        search = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if not search["artists"]["items"]:
            continue
        artist_id = search["artists"]["items"][0]["id"]
        albums = sp.artist_albums(artist_id, album_type="single,album")

        # Get all tracks from all albums
        for album in albums["items"]:
            if album["release_date"] >= date_cutoff:
                tracks = sp.album_tracks(album["id"])["items"]
                new_track_ids.extend([track["id"] for track in tracks])


    return list(set(new_track_ids))


# ----- VIBE FILTER MODULE -----
def filter_tracks_by_vibe(
    sp: spotipy.Spotify, track_ids: List[str], vibe_config: dict
) -> List[str]:
    filtered = []
    features = sp.audio_features(track_ids)

    for f in features:
        if f is None:
            continue
        if (
            f["energy"] >= vibe_config["min_energy"]
            and f["danceability"] >= vibe_config["min_danceability"]
            and f["acousticness"] <= vibe_config["max_acousticness"]
        ):
            filtered.append(f["id"])

    return filtered


# ----- PLAYLIST UPDATER MODULE -----
def add_tracks_to_playlist(sp: spotipy.Spotify, playlist_name: str, track_ids: List[str]):
    if not track_ids:
        print("ℹ️ No tracks to add to playlist.")
        return

    # Create a new playlist
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=f"Automatically generated playlist with new tracks from {', '.join(CONFIG['artists'])}"
    )
    
    # Add tracks to the new playlist
    sp.playlist_add_items(playlist["id"], track_ids)
    print(f"✅ Created new playlist '{playlist_name}' and added {len(track_ids)} tracks.")


# ----- MAIN PIPELINE -----
def run_weekly_playlist_update():
    sp = get_spotify_client()
    print("🎧 Connected to Spotify")

    new_tracks = get_new_tracks(sp, CONFIG["artists"], CONFIG["days_back"])
    print(f"🔍 Found {len(new_tracks)} new tracks")

    # filtered_tracks = filter_tracks_by_vibe(sp, new_tracks, CONFIG["vibe_filter"])
    # print(f"🎯 {len(filtered_tracks)} tracks passed vibe filter")

    add_tracks_to_playlist(sp, CONFIG["playlist_id"], new_tracks)


if __name__ == "__main__":
    run_weekly_playlist_update()
