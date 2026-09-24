# Terminally-Addicted

A curses-based terminal shell that puts Spotify, GitHub issues, Todoist, a GPT chatbot, and YouTube (rendered as ASCII/terminal video) behind one command bar, so you never alt-tab out of the terminal.

Built in 36-ish hours at HackOHI/O 2024 (October 2024). Took Most Original. Demo: https://www.youtube.com/watch?v=SqKeySB5aBU

## What it does

The whole thing runs inside one `curses` window, split into three panes (to-do list, GitHub issues, chatbot) plus a command bar at the bottom. You type a `$`-prefixed command, hit enter, and the relevant pane updates in place — no window switching, no browser tab.

Spotify gets a full remote: search and queue a song, skip, go back, play, pause, all from `$sp` commands hitting the Spotify Web API through `spotipy`. GitHub issues get the same treatment under `$git` — create, close, comment, list, update, search by label — talking straight to the GitHub REST API. `$todo` does the same against the Todoist REST API. `$chat` sends your prompt to GPT-4o-mini and either prints the reply in the right pane or, if it's long, dumps it to a buffer file and opens Vim so you can actually read it.

The odd one out is `/yt` and `$download`: search YouTube, pull the top result with `yt-dlp`, and play it back inside the terminal — video through a Go renderer (the `libs/pot` submodule) synced over a signal handler to audio played with `pydub`, or just download the raw MP4/MP3 if you want the file. `$set env` drops you into Vim on the `.env` file directly, because even your API keys shouldn't require leaving curses.

## How it works

- `terminal/main.py` — the curses event loop: draws the three panes plus command bar, parses `$commands`, dispatches to the right API module, redraws.
- `terminal/helpers.py` — pane rendering helpers (borders, titles, the "if it's too long, open Vim instead" fallback).
- `server/spotify_api.py`, `server/github_api.py`, `server/todoist.py`, `server/youtube_api.py`, `server/chatbot.py` — one thin wrapper per external API (spotipy, GitHub REST, Todoist REST, YouTube Data API, OpenAI).
- `libs/media_player/downloader.py` — pulls video+audio with `yt-dlp`.
- `libs/media_player/term_video.py` — spawns the Go video renderer (`libs/pot` submodule) and an audio thread, synced with a `SIGUSR1` handler.
- API clients read credentials from a root-level `.env` through `python-dotenv`. The
  `$set env` command edits that same file. Start from the included template:

  ```sh
  cp server/.env.template .env
  ```

  Fill in the values you use: `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`,
  `GITHUB_TOKEN`, `TODOIST_API_TOKEN`, `OPENAI_API_KEY`, and `YOUTUBE_API_TOKEN`.
  Keep real credentials in `.env`, never commit them.

## Run

Use Python 3 on a Unix-like terminal with curses and Vim installed. The media player
also needs Go and FFmpeg; YouTube playback depends on the `libs/pot` submodule. Clone
with submodules, install the Python dependencies, then launch from the repository root:

```sh
git clone --recurse-submodules https://github.com/Aryagarg23/Terminally-Addicted.git
cd Terminally-Addicted
python3 -m pip install -r requirements.txt
python3 terminal/main.py
```

The integrations call external APIs and need valid credentials and network access.
Some terminal media playback behavior is platform-specific.

## Diagram

`prototype/command_map.py` draws the shape of the project instead of measuring anything: one curses window in the center, a `$`-command out to each backing service (Spotify, GitHub, Todoist, OpenAI, YouTube's ASCII renderer, Vim for `.env`), and the reply landing back in the same window. No screenshot, no invented metrics — just the map of what talks to what.

Run it locally:

```bash
MPLCONFIGDIR=/home/arya/projects/hackathons/.mplcache \
/home/arya/projects/hackathons/.venv/bin/python prototype/command_map.py
```

![One curses window, six APIs](https://vircgxpcwyvniemqmdyi.supabase.co/storage/v1/object/public/media/writing/Terminally-Addicted/command_map.png)

## Team

- **Arya Garg** ([@Aryagarg23](https://github.com/Aryagarg23)) — built the curses shell, GitHub/Todoist/env integration, chatbot wiring, and the video/audio downloader and player.
- **[Raihan Rafeek](https://www.rai-1975.com/)** ([@rai1975](https://github.com/rai1975)) — terminal pane splitting and Spotify API integration.
- **[Kaaustaaub Shankar](https://kaaustaaub.netlify.app/)** ([@KaaustaaubShankar](https://github.com/KaaustaaubShankar)) — YouTube API and Spotify improvements.

## Links

- Writeup: https://aryagarg23.com/writing/terminally-addicted
- Site: https://aryagarg23.com
- Devpost profile: https://devpost.com/Aryagarg23

## More hackathon builds

- [Gyrus](https://github.com/Aryagarg23/Gyrus) — agentic browser that supports curiosity instead of replacing it (WeaveHacks 2025)
- [WhiteBox](https://github.com/Aryagarg23/WhiteBox) — traceable GraphRAG over medical literature (Future of Data 2024, 1st place)
- [G-Code-Assembler](https://github.com/Aryagarg23/G-Code-Assembler) — G-code assembly + STL visualization (MakeUC 2024, Kinetic Vision winner)
- [Memento](https://github.com/Aryagarg23/Memento) — digital memory journal for Alzheimer's patients and caregivers (RevolutionUC 2024, 3rd overall)
- [Buycott](https://github.com/Aryagarg23/Buycott) — barcode scan -> parent company -> NLP stance on social issues (MakeUC 2023, 1st overall)
- [SignLink](https://github.com/Aryagarg23/SignLink) — video calls with real-time ASL fingerspelling to text (BoilerMake X 2023)
- [Kuka Arm Viz](https://github.com/Aryagarg23/Visualizing-Kuka-7-Node-Robot-Arm) — interactive 7-DOF robot arm in WebGL with inverse kinematics (RevolutionUC 2023)
- [Hi-Five](https://github.com/Aryagarg23/Hi-Five) — anonymous friend-matching on OCEAN personality vectors (SASEhack 2024)
- [Friction](https://github.com/Aryagarg23/Friction) — speculative OS + hardware that protects flow state with physical friction (Fig Build 2026)
