# Spotify Playlist Generator

This application automatically monitors specified artists for new releases and adds them to a designated Spotify playlist.

## Setup

1. Create a Spotify Developer account at https://developer.spotify.com/
2. Create a new application in the Spotify Developer Dashboard
3. Get your Client ID and Client Secret from your application
4. Create a `.env` file in the project root with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application with your preferred schedule:
   ```bash
   # Run daily at midnight (default)
   python spotify_playlist_generator.py

   # Run hourly
   python spotify_playlist_generator.py --schedule hourly

   # Run daily at a specific time
   python spotify_playlist_generator.py --schedule daily --time "14:30"

   # Run weekly on a specific day and time
   python spotify_playlist_generator.py --schedule weekly --day monday --time "09:00"
   ```
2. Follow the authentication process when prompted
3. Add artists to monitor in the `artists.txt` file (one artist name per line)
4. The application will check for new releases according to your specified schedule

## Features

- Monitors specified artists for new releases
- Automatically adds new songs to a designated playlist
- Flexible scheduling options:
  - Hourly checks
  - Daily checks at specified time
  - Weekly checks on specified day and time
- Maintains a list of processed releases to avoid duplicates 