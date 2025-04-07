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
from config import CONFIG

load_dotenv()


# Global variable to store the auth code
auth_code = None
port = 8888


def find_available_port(start_port):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            port += 1


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        # Extract the code from the URL
        if "code=" in self.path:
            auth_code = self.path.split("code=")[1].split("&")[0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")
            # Stop the server
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        # Suppress logging
        return


def start_local_server():
    global port
    port = find_available_port(8888)
    server = HTTPServer(("localhost", port), OAuthHandler)
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
        cache_path=".cache",
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


# ----- PLAYLIST UPDATER MODULE -----
def delete_old_playlists(sp: spotipy.Spotify):
    """Delete any playlists that start with 'New tracks for the week of'"""
    user_id = sp.current_user()["id"]
    playlists = sp.current_user_playlists()
    
    while playlists:
        for playlist in playlists["items"]:
            if playlist["name"].startswith("New tracks for the week of"):
                sp.user_playlist_unfollow(user_id, playlist["id"])
                print(f"🗑️ Deleted old playlist: {playlist['name']}")
        
        if playlists["next"]:
            playlists = sp.next(playlists)
        else:
            break

def add_tracks_to_playlist(
    sp: spotipy.Spotify, playlist_name: str, track_ids: List[str]
):
    if not track_ids:
        print("ℹ️ No tracks to add to playlist.")
        return

    # Create a new playlist
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=f"Automatically generated playlist with new tracks",
    )

    # Add tracks to the new playlist
    sp.playlist_add_items(playlist["id"], track_ids)
    print(
        f"✅ Created new playlist '{playlist_name}' and added {len(track_ids)} tracks."
    )


# ----- MAIN PIPELINE -----
def run_weekly_playlist_update():
    sp = get_spotify_client()
    print("🎧 Connected to Spotify")

    # Delete old playlists first
    delete_old_playlists(sp)
    
    new_tracks = get_new_tracks(sp, CONFIG["artists"], CONFIG["days_back"])
    print(f"🔍 Found {len(new_tracks)} new tracks")

    add_tracks_to_playlist(sp, CONFIG["playlist_id"], new_tracks)


if __name__ == "__main__":
    run_weekly_playlist_update()
