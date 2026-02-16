from cgitb import small
import time

from pypresence import AioPresence
from pypresence.types import ActivityType

class DiscordRPC:
    def __init__(self, clientID):
        self.clientID = clientID
        self.rpc = AioPresence(clientID)
        self.isConnected = False

    async def connect(self):
        try:
            await self.rpc.connect()
            self.isConnected = True
        except:
            self.isConnected = False

    async def updateStatus(self, stats, largeImage="vlc", ifPaused=False):
        if not self.isConnected:
            return
        try:
            def isItPaused(isIt):
                if isIt:
                    return "paused"
                return "playing"

            await self.rpc.update(
                activity_type=ActivityType.LISTENING,
                details=f"{stats['title']}",
                state=f"{stats['artist']}",
                large_image=largeImage,
                small_image=isItPaused(ifPaused),
                large_text=f"{stats['album']}",
                start=time.time() - stats["position"] if not ifPaused else None,
                end=time.time() + (stats["length"] - stats["position"]) if not ifPaused else None,
            )
        except:
            pass

    async def clear(self):
        if self.isConnected:
            await self.rpc.clear()