import os
import re
from time import sleep


def formatTime(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02}:{secs:02}"


def stateThis(state):
    stateUse = ""
    if state == "playing":
        stateUse = ">"
    elif state == "paused":
        stateUse = "||"
    else:
        stateUse = "?"
    return stateUse


def lyricsThis(lyrics, position):
    outputLines = []
    if lyrics and lyrics != "Unknown Lyrics":
        lyrics_lines = lyrics.strip().split("\n")
        timedLyrics = []
        time_pattern = re.compile(r"\[(\d{2}):(\d{2})(?:\.\d{2})?\]\s*(.*)")

        for line in lyrics_lines:
            match = time_pattern.match(line)
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
        else:
            outputLines.extend(lyrics_lines)
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
    print(f"Scrobbled: {scrobbled}")
    print("~~~~~~~~~~~~~~~~~~~~  LYRIC ~~~~~~~~~~~~~~~~~~~~~")
    print(lyricsThis(lyrics, position))

    sleep(refreshRate)
