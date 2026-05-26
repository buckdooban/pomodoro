# CLI Pomodoro Timer Project Plan

## Overview

### Goal
Move Pomodoro Timer cli from last term over to cross-platform TUI and expand featureset

### Terms:
- Block: a user-determined "chunk" of time
- Pomodoro Block: focused study time
- Break Block: unfocused, mind wandering time
- User notified at the end of every block
- Pomodoro block + Break block = Cycle
    * Every Pomodoro block ends in a **Short** Break Block (default 5 minutes)
    * Every fourth Pomodoro block ends in a **Long** Break Block (default 15 minutes)
- Each Cycle increments the Cycle Count, cycle count increments as long as program runs or until you deliberately restart it. 

## Feature List

### Critical path
- Squash known bugs from v1.0
    * Timer hangs after first Break Block
    * Unit mismatch
- Update pomodoro class to include @decorators
- Move Current program over to the TUI "Textual"
- Wire up current functionality in Textual 
- UX improvements
    * Background reflects what part of Cycle user is in
        + Pomodoro (Red background, white text)
        + Short break (Blue background, black text)
        + Long break (Purple background, black text)
    * Keyboard shortcuts for core features
        + `start`
        + `stop`
        + `restart`
        + `skip`
    * Clickable buttons for users that prefer to use a mouse
- Get OS-level notifications to work cross platform
    * Try `desktop-notifier` first, fallback to TUI 
    * I honestly don't have super high hopes for this one, it'll probably all
    have to be handled within Textual. 
- Installable via `pipx`
    * With real working install script
    * see what this `pyproject.toml` file is all about
- Update README.md with all improvements as they happen

### Back burner
- Settings menu
    * Adjust length of Break Blocks and Pomodoro Blocks
    * Change sound notifying user a cycle has completed
- Customization Menu
    * Change sounds by pointing to a file on user's computer.
    * Autostart Next Cycle when Previous Cycle ends
- Indicator in status bar which part of a cycle user is in
    * Pomodoro (Red background, white text)
    * Short break (Blue background, black text)
    * Long break (Purple background, black text)
- Real time countdown in the toolbar on user's computer near where clock and date are
- Integrate with Twilio so user can get a text when it's time to focus
- Port to Lua so it can be a neovim plugin
- Installable via package manager
    * Linux (apt, pacman)
    * Mac (homebrew)
    * Windows (winget)
