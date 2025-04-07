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
        "Mariah the Scientist",
        "SZA",
        "Burna Boy",
        "Jessie Reyez",
        "Frank Ocean",
        "A Boogie Wit Da Hoodie",
        "H.E.R.",
        "Daniel Caesar",
        "The Weeknd",
        "Smiley",
    ],
    # Make the playlist name dynamic, based on the current date
    "playlist_id": f"New tracks for the week of {datetime.now().strftime('%m/%d/%Y')}",
    "days_back": 7,
}
