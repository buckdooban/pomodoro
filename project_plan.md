# CLI Pomodoro Timer Project Plan

## Project overview

### Goal
Build a customizable Pomodoro Timer cli for focused sessions of studying 

### Terms:
- Pomodoro block: focused study time
- Break block: break time
- Pomodoro block + Break block = One cycle
    * Every Pomodoro block ends in a **short break** (default 5 minutes)
    * Every fourth Pomodoro block has a **long break** (default 15 minutes)
- Each cycle increments the Pomodoro Cycle Count
- Restarting the program resets Pomodoro cycle count back to one

### Success Metric
A user is able to go through three Cycles consisting of one focused Pomodoro Block and an unfocused Break Block. The fourth cycle automatically extends the break which goes back to the normal length at the fifth.

## Feature List

### Critical path
- Ability to stop, start, skip, or restart timer cycles
    * `pomo start`
    * `pomo stop`
    * `pomo skip`
    * `pomo restart`
- Real time countdown in the toolbar on user's computer near where clock and date are
- User notified of Cycle completion with system notification in the top-left corner of screen
    * Notification dismissed once clicked, next cycle starts after notification
      dismissed.
    * Notification sound should come through user's speaker or connected
    device
    * notification banner reads "time for a break" when pomodoro block finishes
    * notification banner reads "time to focus" when break block finishes
- Indicator in status bar which part of a cycle user is in
    * Pomodoro (Red background, white text)
    * Short break (Blue background, black text)
    * Long break (Purple background, black text)

### Back burner
- Settings menu
    * Adjust length of breaks and pomodoro blocks
    * Change sound notifying user a cycle has completed
    * System notification automatically goes away when timer goes off at the end of a cycle
- Customization Menu
    * Change sounds by pointing to a file on user's computer.
    * Autostart breaks
    * Autostart pomodoros
- Integrate with Twilio so user can get a text when it's time to focus
- Port to Lua so it can be a neovim plugin
- Make into a package people can install on their own machines from github
    * Linux
    * Mac
    * Windows
