# Spotify Playlist Generator

A Python script that automatically creates playlists of new tracks from your favorite artists on Spotify. The script filters tracks based on audio features like energy, danceability, and acousticness to create playlists that match your preferred vibe.

## Features

- Automatically discovers new tracks from specified artists
- Filters tracks based on audio features (energy, danceability, acousticness)
- Creates a new playlist with the filtered tracks
- Weekly playlist updates with the current date in the playlist name

## Prerequisites

- Python 3.9 or higher
- Spotify Developer Account
- Spotify API Credentials

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/spotify-playlist-generator.git
   cd spotify-playlist-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Spotify API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Add `http://localhost:8888` and `http://localhost:8889` as Redirect URIs in your app settings
   - Copy your Client ID and Client Secret

5. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Spotify API credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. On first run:
   - A browser window will open asking for Spotify authorization
   - Authorize the application
   - The script will create a playlist with new tracks from your specified artists

3. Subsequent runs:
   - The script will use cached credentials
   - No browser authorization needed

## Configuration

Edit the `CONFIG` dictionary in `main.py` to customize:

- `artists`: List of artists to track
- `days_back`: How many days back to look for new tracks
- `vibe_filter`: Audio feature thresholds for filtering tracks
  - `min_energy`: Minimum energy level (0.0 to 1.0)
  - `min_danceability`: Minimum danceability (0.0 to 1.0)
  - `max_acousticness`: Maximum acousticness (0.0 to 1.0)

## Security

- Never commit your `.env` file or `.cache` files
- Keep your Spotify API credentials secure
- The `.gitignore` file is configured to prevent accidental commits of sensitive data