import asyncio
import json
import os
import subprocess
import time
from sys import platform

from src.discordrpc import DiscordRPC
from src.fetching import getVlcStatus
from src.front.simpleTerm import fetchThose
from src.lastfm import LastFM
import src.util.print as print

class VlcApp:
    def __init__(self, config):
        self.config = config
        self.lastTrackID = None
        self.currentArt = "vlc"
        self.scrobbled = False
        self.isShowing = False
        self.vlc_process = None

    def startup(self):
        path = ""
        if platform == "win32":
            if os.path.exists("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"):
                path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
            elif os.path.exists("C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"):
                path = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
        elif platform == "darwin":
            if os.path.exists("/Applications/VLC.app/Contents/MacOS/VLC"):
                path = "/Applications/VLC.app/Contents/MacOS/VLC"
            elif os.path.exists("/Applications/VLC.app"):
                path = "/Applications/VLC.app"
        elif platform == "linux":
            if os.path.exists("/usr/bin/vlc"):
                path = "/usr/bin/vlc"
            elif os.path.exists(
                "/var/lib/flatpak/app/org.videolan.VLC/x86_64/stable/active/export/bin/org.videolan.VLC"
            ):
                path = "/var/lib/flatpak/app/org.videolan.VLC/x86_64/stable/active/export/bin/org.videolan.VLC"
            elif os.path.exists("/snap/bin/vlc"):
                path = "/snap/bin/vlc"

        if path:
            self.vlc_process = subprocess.Popen([path, "--extraintf=http"])
        else:
            print.error("VLC not found or unsupported platform.")

    async def run(self):
        self.startup()
        self.rpc = DiscordRPC(self.config["discordID"])
        self.lfm = LastFM(
            self.config["lfmKey"],
            self.config["lfmSecret"],
            self.config["lfmUser"],
            self.config["lfmPass"],
        )
        await self.rpc.connect()
        await self.fetcherLoop()

    async def fetcherLoop(self):
        await asyncio.sleep(0.1)

        while True:
            if self.vlc_process and self.vlc_process.poll() is not None:
                print("VLC closed. Exiting...")
                await self.rpc.clear()
                return

            status = getVlcStatus(self.config["vlcPassword"], self.config["vlcPort"])

            if isinstance(status, dict):
                fetchThose(
                    status["title"],
                    status["artist"],
                    status["album"],
                    status["state"],
                    status["position"],
                    status["length"],
                    self.config["refreshRate"],
                    self.scrobbled,
                    status["lyrics"],
                )
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print(status)

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

                if not self.scrobbled and status["length"] > 30:
                    threshold = min(status["length"] / 2, 240)
                    if status["position"] >= threshold:
                        self.lfm.scrobble(
                            status["artist"],
                            status["title"],
                            status["album"],
                            int(time.time()),
                        )
                        self.scrobbled = True
            else:
                if self.isShowing:
                    await self.rpc.clear()
                    self.isShowing = False
                    self.scrobbled = False

            await asyncio.sleep(self.config["refreshRate"])


def loadConfig():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    elif os.path.exists("VLC.UTILS.CONFIG.json"):
        with open("VLC.UTILS.CONFIG.json", "r") as f:
            config = json.load(f)
    else:
        print.error("Config not found.")
        exit()
    return config


if __name__ == "__main__":
    config = loadConfig()

    app = VlcApp(config)
    asyncio.run(app.run())
