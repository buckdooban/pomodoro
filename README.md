# Pomodoro CLI Timer

If you're here from CS 162 
- [here is the YouTube link for the demo](https://youtu.be/CtKZ6L9V6YI)
- [here is the YouTube link for the walkthrough](https://youtu.be/_TJGTeyT6eo)

## Description
A very slick, very cool, fully interactive Pomodoro timer that runs entirely in your terminal. 
Built with [Textual](https://textual.textualize.io/) in the backwards podunk state of Idaho.

## Compatibility
The Texual docs promised me cross platform and by golly that's what I hope you get. 
Cross-platform testing is ongoing so ymmv.

## Requirements
- Python 3.11+
- `textual`

## Installation

**Note:** At the time of this writing it's only been tested on Mac and Ubuntu Linux (I use Linux btw) Windows environments is in progress.
If you're running Windows, it should work. But I'm not 100% sure. The only Windows machine I have is an old Dell Chromebook that I haven't opened since 2021. So, ymmv for a little bit Windows gang. 

If you're feeling frisky and wanna play with it, clone the repo and run it. I intend to get an install script here soon to make it easier for all OS's.

```bash
git clone https://github.com/buckdooban/pomodoro.git
cd pomodoro
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## How It Works

The timer is broken into a **Focus Session** and a **Break**. Focus Session + Break = One **Cycle**
Every fourth cycle gives you a **Long Break**. The session count keeps incrementing but only so you have an idea how long you've been working for.

Focus sessions default to 25 minutes, breaks default to 5, and long breaks are 15.

Currently the only way to change this is by updating the hardcoded values in pomoclass.py but a settings menu that you can toggle from the UI and adjust to your liking is on the roadmap fosho. 

### Keyboard shortcuts


| Key | Action |
|-----|--------|
| `s` | Start timer |
| `p` | Pause timer |
| `n` | Skip to next session |
| `r` | Reset to beginning |
| `d` | Toggle dark mode |
