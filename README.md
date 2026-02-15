# VLC.UTILS

Hi! This is a sleek TUI utility that bridges VLC Media Player with Discord Rich Presence and Last.fm scrobbling.

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
   - Enter your VLC password, Discord Client ID, and Last.fm API credentials.

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

### Download the software from github releases
1. Head on over to https://github.com/daveberrys/VLC.UTILS/releases
2. Download the latest and download the one that's compatible with your operating system
3. Create a new folder
4. Move `VLC.UTILS` to the new folder
5. Create the `config.json` and configure the file.
6. Open the software

> [!CAUTION]
> Some of the code is made by AI (Gemini 3.0 Flash). But I've taken quiz from them and checked the code and everything is fine. Don't worry about your shit being stolen.