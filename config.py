from datetime import datetime

CONFIG = {
    "artists": [
        "Drake",
        "Travis Scott",
        "Kendrick Lamar",
        "J. Cole",
        "Nicki Minaj",
        "Lil Uzi Vert",
        "Post Malone",
        "Travis Scott",
        "Kendrick Lamar",
        "J. Cole",
        "Nicki Minaj",
        "Lil Uzi Vert",
        "Post Malone",
        "Giveon",
    ],
    # Make the playlist name dynamic, based on the current date
    "playlist_id": f"New tracks for the week of {datetime.now().strftime('%m/%d/%Y')}",
    "days_back": 7,
}
