import requests

def fetchAlbumArt(artist: str, track: str) -> str:
    query = f"{artist} {track}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
    
    resp = requests.get(url)
    data = resp.json()
    
    if data["resultCount"] == 0:
        return "vlc"
    
    artworkURL = data["results"][0]["artworkUrl100"]
    artworkURL = artworkURL.replace("100x100bb", "1000x1000bb")
    return artworkURL