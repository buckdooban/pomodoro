# Pomodoro CLI Timer

## Description
A very slick, very cool, fully interactive Pomodoro timer that runs entirely in your terminal. 
Built with [Textual](https://textual.textualize.io/) in the backwards podunk state of Idaho.

## Compatibility
The Texual docs promised me cross platform and by golly that's what I hope you get. At the time of this writing it's only been tested on Ubuntu Linux. 
Cross-platform testing is ongoing so ymmv.

## Requirements
- Python 3.11+
- `textual`

## Installation

```bash
pip install git+https://github.com/buckdooban/pomodoro.git
```

Or clone and run manually:

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

Currently the only way to change this is by updating the hardcoded values but a settings menu that you can toggle from the UI and adjust to your liking is on the roadmap fosho. 

### Keyboard shortcuts


| Key | Action |
|-----|--------|
| `s` | Start timer |
| `p` | Pause timer |
| `n` | Skip to next session |
| `r` | Reset to beginning |
| `d` | Toggle dark mode |
