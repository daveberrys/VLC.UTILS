import pylast
import src.util.print as print

class LastFM:
    def __init__(self, apiKey, apiSecret, username, password):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.username = username
        self.passwordHash = pylast.md5(password)
        try:
            self.network = pylast.LastFMNetwork(
                api_key=apiKey,
                api_secret=apiSecret,
                username=username,
                password_hash=self.passwordHash,
            )
        except:
            self.network = None

    def getAlbumArt(self, artist, track):
        artist = artist.split(",")[0].strip()
        try:
            trackObj = self.network.get_track(artist, track)
            albumObj = trackObj.get_album()
            if albumObj:
                art = albumObj.get_cover_image(pylast.SIZE_MEGA)
                if art:
                    return art
            return "vlc"
        except:
            return "vlc"

    def updateNowPlaying(self, artist, track, album):
        if not self.network:
            return
        artist = artist.split(",")[0].strip()
        try:
            self.network.update_now_playing(artist=artist, title=track, album=album)
        except Exception as e:
            print.error(f"Updating failed: {e}")

    def scrobble(self, artist, track, album, timestamp):
        if not self.network:
            return
        artist = artist.split(",")[0].strip()
        try:
            self.network.scrobble(
                artist=artist, title=track, album=album, timestamp=timestamp
            )
        except Exception as e:
            print.error(f"Scrobbing failed: {e}")
