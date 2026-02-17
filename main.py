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
from src.itunesArt import fetchAlbumArt

class VlcApp:
    def __init__(self, config):
        self.config = config
        self.lastTrackID = None
        self.currentArt = "vlc"

        self.playedTime = 0
        self.lastPosition = 0
        self.lastHeartbeat = 0

        self.scrobbled = False
        self.previousState = None
        self.trackStartTime = None
        self.vlcProcess = None

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
            self.vlcProcess = subprocess.Popen([path, "--extraintf=http"])
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
            if self.vlcProcess and self.vlcProcess.poll() is not None:
                print("VLC closed. Exiting...")
                await self.rpc.clear()
                os._exit(0)

            status = getVlcStatus(
                self.config["vlcPassword"],
                self.config["vlcPort"]
            )

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

            if not isinstance(status, dict):
                await asyncio.sleep(self.config["refreshRate"])
                continue

            state = status["state"]
            position = int(status["position"])
            length = int(status["length"])
            trackID = f"{status['title']} - {status['artist']}"

            # funky discord RPC shit
            if self.previousState == "playing" and state == "paused":
                await self.rpc.updateStatus(status, self.currentArt, True)
            elif self.previousState == "paused" and state == "playing":
                await self.rpc.updateStatus(status, self.currentArt, False)
            elif state == "stopped":
                await self.rpc.updateStatus(status, self.currentArt, True)

            if state == "playing":
                if trackID != self.lastTrackID:
                    self.currentArt = fetchAlbumArt(
                        status["artist"],
                        status["title"]
                    )

                    self.lfm.updateNowPlaying(
                        status["artist"],
                        status["title"],
                        status["album"]
                    )

                    await self.rpc.updateStatus(status, self.currentArt, False)
                    self.lastHeartbeat = time.time()

                    self.lastTrackID = trackID
                    self.scrobbled = False
                    self.playedTime = 0
                    self.lastPosition = position
                    self.trackStartTime = int(time.time()) - position

                if time.time() - self.lastHeartbeat >= 15:
                    self.lfm.updateNowPlaying(
                        status["artist"],
                        status["title"],
                        status["album"]
                    )
                    self.lastHeartbeat = time.time()

                if self.lastTrackID == trackID:
                    delta = position - self.lastPosition
                    if 0 <= delta <= 3:
                        self.playedTime += delta
                    elif abs(delta) > 5:
                        self.lastPosition = position
                    self.lastPosition = position

                    if (
                        not self.scrobbled
                        and length > 30
                        and self.trackStartTime is not None
                    ):
                        threshold = min(length / 2, 240)

                        if self.playedTime >= threshold:
                            self.lfm.scrobble(
                                status["artist"],
                                status["title"],
                                status["album"],
                                self.trackStartTime
                            )
                            self.scrobbled = True
            if state == "paused" and self.previousState == "playing":
                pass

            self.previousState = state
            await asyncio.sleep(self.config["refreshRate"])


def loadConfig():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    elif os.path.exists("VLC.UTILS.CONFIG.json"):
        with open("VLC.UTILS.CONFIG.json", "r") as f:
            config = json.load(f)
    else:
        print.fatal("Config not found.")
        exit()
    return config


if __name__ == "__main__":
    config = loadConfig()

    app = VlcApp(config)
    asyncio.run(app.run())
