# Spotify Playlist Generator

This application automatically monitors specified artists for new releases and adds them to a designated Spotify playlist. It includes both a command-line interface and a web UI.

## Features

- Monitors specified artists for new releases
- Automatically adds new songs to a designated playlist
- Flexible scheduling options:
  - Hourly checks
  - Daily checks at specified time
  - Weekly checks on specified day and time
- Maintains a list of processed releases to avoid duplicates
- Modern web interface for easy management
- Command-line interface for automated running

## Setup

1. Create a Spotify Developer account at https://developer.spotify.com/
2. Create a new application in the Spotify Developer Dashboard
3. Get your Client ID and Client Secret from your application
4. Add `http://localhost:3000/callback` to your application's Redirect URIs in the Spotify Dashboard

### Backend Setup

1. Create a `.env` file in the project root with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Web UI Setup

1. Navigate to the UI directory:
   ```bash
   cd ui
   ```

2. Create a `.env.local` file with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:3000/callback
   SPOTIFY_PLAYLIST_ID=your_playlist_id
   ```

3. Install the required dependencies:
   ```bash
   npm install
   ```

## Usage

### Running the Backend Script

Run the application with your preferred schedule:
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

### Running the Web UI

1. Start the development server:
   ```bash
   cd ui
   npm run dev
   ```

2. Open your browser and navigate to `http://localhost:3000`

3. The first time you visit the site, you'll be redirected to Spotify for authentication
4. After authenticating, you can:
   - Add/remove artists to monitor
   - Configure the schedule
   - View the current playlist status

## Managing Artists

### Using the Web UI
1. Log in to the web interface
2. Use the "Add Artist" form to add new artists
3. Click "Remove" next to any artist to remove them from monitoring

### Using the Command Line
1. Edit the `artists.txt` file in the project root
2. Add one artist name per line
3. Save the file and the application will automatically pick up the changes

## Notes

- The web UI requires a modern browser with JavaScript enabled
- The backend script can run on any system with Python 3.7+
- Both interfaces use the same underlying functionality
- The web UI provides a more user-friendly way to manage artists and schedules
- The command-line interface is better suited for automated running on servers 