import os
import re
from time import sleep

def formatTime(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02}:{secs:02}"

def stateThis(state):
    if state == "playing":
        return ">"
    elif state == "paused":
        return "||"
    else:
        return "?"

def scrobbledThis(scrobble, invalidated, length):
    threshold = int(min(length / 2, 240))
    formattedTresh = formatTime(threshold)

    if invalidated:
        if scrobble:
            return f"{scrobble} (Paused) ({formattedTresh})"
        return f"{scrobble} (Invalidated) ({formattedTresh})"
    else:
        return f"{scrobble} ({formattedTresh})"


def lyricsThis(lyrics, position):
    outputLines = []
    if lyrics and lyrics != "Unknown Lyrics":
        lyricsLines = lyrics.strip().split("\n")
        timedLyrics = []
        timePattern = re.compile(r"\[(\d{2}):(\d{2})(?:\.\d{2})?\]\s*(.*)")

        for line in lyricsLines:
            match = timePattern.match(line)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                text = match.group(3)
                timedLyrics.append({"time": minutes * 60 + seconds, "text": text})

        if timedLyrics:
            currentLyricText = "..."
            for i in range(len(timedLyrics)):
                if timedLyrics[i]["time"] <= position:
                    currentLyricText = timedLyrics[i]["text"]
                    if (
                        i + 1 < len(timedLyrics)
                        and position < timedLyrics[i + 1]["time"]
                    ):
                        break
                elif timedLyrics[i]["time"] > position:
                    break
            outputLines.append(f"{currentLyricText}")
        elif outputLines == []:
            outputLines.append("...")
        else:
            outputLines.extend(lyricsLines)
    else:
        outputLines.append("No lyrics available.")
    return "\n".join(outputLines)


def fetchThose(
    song,
    artist,
    album,
    state,
    position,
    length,
    refreshRate,
    scrobbled,
    invalidated,
    lyrics,
):
    os.system("cls" if os.name == "nt" else "clear")

    print("~~~~~~~~~~~~~~~~~~~ VLC.UTILS ~~~~~~~~~~~~~~~~~~~")
    print(f"Song: {song}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"{stateThis(state)} - {formatTime(position)} / {formatTime(length)}")
    print("~~~~~~~~~~~~~~~~~~~~ LAST.FM ~~~~~~~~~~~~~~~~~~~~")
    print(f"Scrobbled: {scrobbledThis(scrobbled, invalidated, length)}")
    print(f"Invalidated: {invalidated}")
    print("~~~~~~~~~~~~~~~~~~~~  LYRIC ~~~~~~~~~~~~~~~~~~~~~")
    print(lyricsThis(lyrics, position))

    sleep(refreshRate)
