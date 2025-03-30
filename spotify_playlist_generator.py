import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime, timedelta
import argparse

# Load environment variables
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')

# Scope for required permissions
SCOPES = [
    'playlist-modify-public',
    'playlist-read-private',
    'user-read-email',
    'user-read-private'
]

class SpotifyPlaylistGenerator:
    def __init__(self):
        self.sp = None
        self.processed_releases = set()
        self.playlist_id = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Spotify using Authorization Code with refresh token"""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=' '.join(SCOPES),
            cache_path='.spotify_caches'
        ))

    def create_playlist(self, name="New Releases Playlist"):
        """Create a new playlist if it doesn't exist"""
        user_id = self.sp.current_user()['id']
        playlists = self.sp.user_playlists(user_id)
        
        # Check if playlist already exists
        for playlist in playlists['items']:
            if playlist['name'] == name:
                self.playlist_id = playlist['id']
                return
        
        # Create new playlist if it doesn't exist
        playlist = self.sp.user_playlist_create(
            user_id,
            name,
            public=True,
            description="Automatically updated playlist with new releases from monitored artists"
        )
        self.playlist_id = playlist['id']

    def load_artists(self):
        """Load artists from artists.txt file"""
        try:
            with open('artists.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("artists.txt not found. Creating new file.")
            with open('artists.txt', 'w') as f:
                f.write("")
            return []

    def load_processed_releases(self):
        """Load processed releases from processed_releases.json"""
        try:
            with open('processed_releases.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def save_processed_releases(self):
        """Save processed releases to processed_releases.json"""
        with open('processed_releases.json', 'w') as f:
            json.dump(list(self.processed_releases), f)

    def check_new_releases(self):
        """Check for new releases from monitored artists"""
        print(f"Checking for new releases at {datetime.now()}")
        
        artists = self.load_artists()
        if not artists:
            print("No artists found in artists.txt")
            return

        # Get current date and date 30 days ago
        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)

        for artist_name in artists:
            # Search for the artist
            results = self.sp.search(q=artist_name, type='artist', limit=1)
            if not results['artists']['items']:
                print(f"Artist not found: {artist_name}")
                continue

            artist_id = results['artists']['items'][0]['id']
            
            # Get artist's albums
            albums = self.sp.artist_albums(artist_id, album_type='album,single')
            
            for album in albums['items']:
                release_date = datetime.strptime(album['release_date'], '%Y-%m-%d')
                
                # Check if release is within the last 30 days
                if thirty_days_ago <= release_date <= current_date:
                    album_id = album['id']
                    
                    # Skip if already processed
                    if album_id in self.processed_releases:
                        continue
                    
                    # Get tracks from the album
                    tracks = self.sp.album_tracks(album_id)
                    track_uris = [track['uri'] for track in tracks['items']]
                    
                    # Add tracks to playlist
                    if track_uris:
                        self.sp.playlist_add_items(self.playlist_id, track_uris)
                        print(f"Added {len(track_uris)} tracks from {album['name']} by {artist_name}")
                        self.processed_releases.add(album_id)
        
        # Save processed releases
        self.save_processed_releases()

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Spotify Playlist Generator')
    parser.add_argument('--schedule', choices=['hourly', 'daily', 'weekly'], default='daily',
                      help='Schedule interval (default: daily)')
    parser.add_argument('--time', default='00:00',
                      help='Time to run the check (for daily/weekly schedule, format: HH:MM)')
    parser.add_argument('--day', choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                      help='Day of the week to run the check (for weekly schedule)')
    args = parser.parse_args()

    generator = SpotifyPlaylistGenerator()
    generator.create_playlist()
    
    # Run initial check
    generator.check_new_releases()
    
    # Schedule based on command line arguments
    if args.schedule == 'hourly':
        schedule.every().hour.do(generator.check_new_releases)
        print(f"Will check for new releases every hour")
    elif args.schedule == 'daily':
        schedule.every().day.at(args.time).do(generator.check_new_releases)
        print(f"Will check for new releases daily at {args.time}")
    elif args.schedule == 'weekly':
        if not args.day:
            print("Error: --day argument is required for weekly schedule")
            return
        getattr(schedule.every(), args.day).at(args.time).do(generator.check_new_releases)
        print(f"Will check for new releases every {args.day} at {args.time}")
    
    print("Spotify Playlist Generator is running. Press Ctrl+C to exit.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 