from datetime import datetime

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