import asyncio
import time
import json
from src.fetching import getVlcStatus
from src.discordrpc import DiscordRPC
from src.lastfm import LastFM
from src.front.tui import VlcTui

class VlcApp(VlcTui):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.lastTrackID = None
        self.currentArt = "vlc"
        self.scrobbled = False
        self.isShowing = False

    async def on_mount(self):
        self.rpc = DiscordRPC(self.config["discordID"])
        self.lfm = LastFM(
            self.config["lfmKey"],
            self.config["lfmSecret"],
            self.config["lfmUser"],
            self.config["lfmPass"],
        )
        await self.rpc.connect()
        self.run_worker(self.fetcherLoop())

    async def fetcherLoop(self):
        await asyncio.sleep(0.1)
        while True:
            status = getVlcStatus(self.config["vlcPassword"], self.config["vlcPort"])

            if isinstance(status, dict) and status["state"] == "playing":
                trackID = f"{status['title']} - {status['artist']}"

                if trackID != self.lastTrackID:
                    self.currentArt = self.lfm.getAlbumArt(
                        status["artist"], status["title"]
                    )
                    self.lfm.updateNowPlaying(
                        status["artist"], status["title"], status["album"]
                    )
                    await self.rpc.updateStatus(status, self.currentArt)
                    self.lastTrackID = trackID
                    self.scrobbled = False
                    self.isShowing = True

                elif not self.isShowing:
                    self.lfm.updateNowPlaying(
                        status["artist"], status["title"], status["album"]
                    )
                    await self.rpc.updateStatus(status, self.currentArt)
                    self.isShowing = True

                if not self.scrobbled and status["length"] > 30:
                    threshold = min(status["length"] / 2, 240)
                    if status["position"] >= threshold:
                        self.lfm.scrobble(
                            status["artist"],
                            status["title"],
                            status["album"],
                            int(time.time()),
                        )
                        self.lfm.updateNowPlaying(
                            status["artist"], status["title"], status["album"]
                        )
                        self.scrobbled = True

                self.updateInfo(status, self.currentArt)

            elif isinstance(status, dict) and status["state"] != "playing":
                if self.isShowing:
                    await self.rpc.clear()
                    self.isShowing = False
                self.updateInfo(status, self.currentArt)

            await asyncio.sleep(self.config["refreshRate"])


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)

    app = VlcApp(config)
    app.run()