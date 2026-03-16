# Pomodoro CLI Timer

## Description
A very slick, very cool, interactive command-line Pomodoro timer. Allows users to run a structured focus/break timer via the terminal.

## Environment & Compatibility Notice
**I use Linux btw:** At this stage in the project I have selfishly only developed on my Linux machine but plan to make this as cross-platform as I can as time permits.

The system-level notifcations are handled by [desktop-notifier](https://desktop-notifier.readthedocs.io/en/latest/#) and I had to cry for at least an entire afternoon to get them to work on my machine properly so ymmv if you try and get it to run locally. 

## Prerequisites & Installation
Python 3.9+ and the `desktop-notifier` package.

1. Download the zip file, extract in a folder named "stolen_nft_screenshots" 
2. Open your terminal and navigate inside the extracted project folder.
3. Create the virtual environment (not required, but a good idea):
   - `python3 -m .venv venv`
4. Activate the environment: 
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
5. Install dependencies:
   `pip install -r requirements.txt`

## Usage
Boot it up with:
`python main.py`

Once the timer is running, you can type the following commands into the terminal and press Enter:
* `pause` - Suspends the active timer.
* `start` - Resumes a paused timer.
* `skip`  - Instantly ends the current phase and moves to the next (e.g., skips a break).
* `reset` - Restarts the current phase from the beginning.
* `stop`, `quit`, or `:q`- Terminates the application.

## Helpful for peer reviews

Just so you don't have to go read the docs like a dork like I did here's the 411 on the stuff that isn't self explanatory: 

**1. Asynchronous Execution (`asyncio`)**
Standard Python scripts execute one line at a time. If a program waits for a user to type a command (`input("et tu, Brutus? ")`), the whole program stops and waits. This project uses the `asyncio` event loop and thread executors (`asyncio.to_thread`) to make it seems like we're running the countdown timer and the user input listener concurrently. This allows the timer to update visually every second while constantly listening for your keyboard commands in the background.

**2. State Management via Async Events**
Instead of using standard boolean variables, I'm using fancy schmancy `asyncio.Event` flags to communicate what gets picked up by the input thread to the timer loop safely. When you type `pause`, the input thread sets the `pause_event` flag, and the timer loop reacts to it on its next tick.

**3. Desktop Notifications**
The `desktop-notifier` package handles all the scary communication with the OS's hardware. When a timer phase ends, the event loop pauses and sends a request to the OS to trigger a cute little popup. The loop remains paused until the user interacts with the notification, which triggers a callback to resume the application.
