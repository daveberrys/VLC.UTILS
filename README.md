<div align="center">
   <img src="icon/VLC.UTILS.png" width=150 height=150 alt="VLC.UTILS"/>
   <h1> VLC.UTILS </h1>
   <span> A sleek TUI utility that bridges VLC Media Player with Discord Rich Presence and Last.fm scrobbling. </span> <br/>
   <span> Available for Windows, macOS and Linux. </span> <br/>
   
   <img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
   <!-- <img src="https://img.shields.io/badge/Intergraded%20with-Last.fm-D51007?style=flat-square&logo=last.fm&logoColor=white"/>
   <img src="https://img.shields.io/badge/Intergraded%20with-Discord%20RPC-5663f7?style=flat-square&logo=discord&logoColor=white"/> -->
</div>

## Features
- **Discord RPC**: Shows what you're listening to with sync timers and high-quality album art.
- **Last.fm**: Automatic "Now Playing" updates and threshold-based scrobbling.
- **TUI**: A beautiful terminal interface with a live progress bar and album info.
- **Cross-Platform**: Ready to be compiled for Windows, macOS, and Linux.

## Setup
1. **VLC Configuration**:
   - Open VLC -> Tools -> Preferences -> All.
   - Interface -> Main interfaces -> Check "Web".
   - Interface -> Main interfaces -> Lua -> Set a **Lua Password** (e.g., `helloworld`).
2. **Settings**:
   - Create a config.json in the root folder (see config.json template).
   - Enter your VLC password, Discord Application Client ID (Not your UserID), and Last.fm API credentials.

## Running the software
### Running the software from source
1. Make sure you have [Python](https://python.org/) installed.
2. Clone the repository and navigate into it.
3. Open the `config.json` and configure the file.
4. Open Powershell (Reccomended) or Command Prompt.
5. Create a virtual environment: `python -m venv venv`
6. Install dependencies: `pip install -r requirements.txt`
7. Run: `python main.py`

### Compile the software from source
1. Make sure you have [Python](https://python.org/) installed.
2. Clone the repository and navigate into it.
3. Open Powershell (Reccomended) or Command Prompt.
4. Create a virtual environment: `python -m venv venv`
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `pyinstaller build.spec`
7. Navigate to `dist/`
8. Create the `config.json` and configure the file.
9. Open the software

### Download the software from nightly.link
1. Download the one that's compatible with your operating system
  - Windows: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-Windows.zip
  - macOS: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-MacOS.zip
  - Linux: https://nightly.link/daveberrys/VLC.UTILS/workflows/building/main/VLC.UTILS-Linux.zip
2. Create a new folder
3. Move `VLC.UTILS` to the new folder
4. Create the `config.json` and configure the file.
5. Open the software

> [!CAUTION]
> Some of the code is made by AI (Gemini 3.0 Flash). But I've taken quiz from them and checked the code and everything is fine. Don't worry about your shit being stolen.