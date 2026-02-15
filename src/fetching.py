import requests
from requests.auth import HTTPBasicAuth

def getVlcStatus(password, port, host="localhost"):
    url = f"http://{host}:{port}/requests/status.json"
    try:
        response = requests.get(url, auth=HTTPBasicAuth('', password))
        if response.status_code == 200:
            data = response.json()
            meta = data.get('information', {}).get('category', {}).get('meta', {})
            return {
                "title": meta.get('title', 'Unknown Title'),
                "artist": meta.get('artist', 'Unknown Artist'),
                "album": meta.get('album', 'Unknown Album'),
                "lyrics": meta.get('LYRICS', 'Unknown Lyrics'),
                "position": data.get('time', 0),
                "length": data.get('length', 0),
                "state": data.get('state', 'stopped')
            }
        return f"Error: Bad Status: {response.status_code}"
    except Exception as e:
        return f"Error: Connection Failed: {e}"