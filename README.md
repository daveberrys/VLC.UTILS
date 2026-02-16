<div align="center">
   <img src="icon/VLC.UTILS.png" width=150 height=150 alt="VLC.UTILS"/>
   <h1> VLC.UTILS </h1>
   <span> A sleek Python Project utility that bridges VLC Media Player with Discord Rich Presence and Last.fm scrobbling. </span> <br/>
   <span> Available for Windows, macOS and Linux. </span> <br/>
   
   <img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white"/> <br/>
   <!-- <img src="https://img.shields.io/badge/Intergraded%20with-Last.fm-D51007?style=flat-square&logo=last.fm&logoColor=white"/>
   <img src="https://img.shields.io/badge/Intergraded%20with-Discord%20RPC-5663f7?style=flat-square&logo=discord&logoColor=white"/> -->
   
   <img src="readme/Preview.png" alt="preview"/>
</div>

## Features
- **Discord RPC**: Shows what you're listening to with sync timed and album art.
- **Last.fm**: Automatic "Now Playing" updates and threshold-based scrobbling.
- **iTunes**: Automatically fetches the Album art from iTunes.
- **Cross-Platform**: Ready to be compiled for Windows, macOS, and Linux.

## Prerequisites
- [VLC Media Player](https://www.videolan.org/vlc/) (bits don't matter, they're countered.)
- [Offical Discord](https://discord.com/download) running the background or [arRPC](https://github.com/OpenAsar/arRPC)
- A [LastFM](https://www.last.fm/) account, with [LastFM API and Secret keys](https://www.last.fm/api/accounts).

## Setup
1. **Settings**:
   - Create a `config.json` in the root folder.
   - Copy this json code:
   ```json
   {
      "vlcPassword": "",
      "vlcPort": "8080",
      "discordID": "1451462308533637212",

      "lfmKey": "",
      "lfmSecret": "",
      "lfmUser": "",
      "lfmPass": "",

      "refreshRate": 0.5
   }
   ```
   - Paste it in the `config.json`.
   - Enter your VLC password, and Last.fm API, Secret and credentials.
      - Extra notes:
         - `discordID` is my application ID! You can change it, but not reccomended.
         - `vlcPort` may be different. Please check your port in VLC settings.
         - `refreshRate` is set to `0.5` for performance reasons. Lowering it might be too laggy and **will** flicker.
      - Why your credidentals?
      - How else are we gonna scrobble the songs for you dummy?
      - Also, we're open source and we don't take anything from you whatsoever.
2. **Opening the app**:
   - Just open the tool and that's it.

## Running the tool
### Download the tool from nightly.link (Reccomended)
1. Download the one that's compatible with your operating system
      - Windows: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-Windows.zip
      - macOS: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-MacOS.zip
      - Linux: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-Linux.zip
2. Create a new folder
3. Move `VLC.UTILS` to the new folder
4. Create the `config.json` and configure the file.
5. Open the tool

### Running the tool from source
1. Make sure you have [Python](https://python.org/) installed.
2. Clone the repository and navigate into it.
3. Open the `config.json` and configure the file.
4. Open Powershell (Reccomended) or Command Prompt.
5. Create a virtual environment: `python -m venv venv`
6. Install dependencies: `pip install -r requirements.txt`
7. Run: `python main.py`

### Compile the tool from source
1. Make sure you have [Python](https://python.org/) installed.
2. Clone the repository and navigate into it.
3. Open Powershell (Reccomended) or Command Prompt.
4. Create a virtual environment: `python -m venv venv`
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `pyinstaller build.spec`
7. Navigate to `dist/`
8. Create the `config.json` and configure the file.
9. Open the tool

> [!IMPORTANT]
> Some of the code is made by AI (Gemini 3.0 Flash). But I've taken quiz from them and checked the code and everything is fine. Don't worry about your shit being stolen. The reason why I use LLMs is because of two things. ADHD and short-term memory loss. I struggle with trying to remember things and I need the usage of LLM to help me out on giving me quizzes so I remember and I re-learn it again.
