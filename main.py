import pomoclass
import subprocess
import platform
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Static

pomo = pomoclass.PomodoroManager()

# TODO: Installable via `pipx`
# ___ With real working cross-OS install script
# TODO: refactor the rest of the classes in PomodoroManager to use decorators as it becomes necessary
# e.g. when user input starts happening
# TODO: see if there is a replacement for or if you can get DesktopNotifier to work for system-level notifications
# TODO: initialize all of the default state/ provide customization options with a config file instead of hard coding
# TODO: settings menu: provide capabilities to adjust default settings/ customize from UI
# - [ ] Adjust length of Break Blocks and Pomodoro Blocks
# - [ ] Change notification sound
# - [ ] Optionally Autostart Next Cycle when Previous Cycle ends
# TODO: Background color changes depending on what part of cycle you're in
# - [ ] Focus (Red background, white text)
# - [ ] Short break (Blue background, black text)
# - [ ] Long break (Purple background, black text)
# TODO: Real time countdown in the toolbar on user's computer near where clock and date are
# maybe adjust the background color too?
# TODO: SMS notifications
# Integrate with Twilio so user can get a text when it's time to focus
# TODO: Update README.md
# screenshots


class TimeDisplay(Digits):
    """Widget displaying timer face"""

    timer_duration = pomo.timer_duration
    focus_duration = pomo.FOCUS_SESSION_DURATION

    start_time = timer_duration
    time = reactive(timer_duration)

    sound_path = Path(__file__).parent / "tone.wav"

    def on_mount(self) -> None:
        """event handler called when a widget is added to the app"""
        self.update_timer = self.set_interval(1, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method updates time to current time"""
        self.time -= 1

    # methods prefixed watch_ followed by name of reactive attribute
    # run every time the reactive attribute changes
    def watch_time(self, time: int) -> None:
        """Called when the time attribute changes."""
        mins, secs = divmod(time, 60)
        if time == 0:
            self.update_session()
            self.play_notification()
        else:
            self.update(f"{mins:02.0f}:{secs:02.0f}")

    def play_notification(self):
        if platform.system() == "Linux":
            subprocess.Popen(["aplay", self.sound_path])
        elif platform.system() == "Darwin":
            subprocess.Popen(["afplay", self.sound_path])
        elif platform.system() == "Windows":
            subprocess.Popen(
                [
                    "powershell",
                    "-c",
                    f"(New-Object Media.SoundPlayer '{self.sound_path}').PlaySync()",
                ]
            )

    def sync_ui(self):
        # update cycle count in UI
        self.app.query_one(Cycles).update_cycle()
        # update current session in UI
        self.app.query_one(Current_Session).update_current_session()
        self.time = pomo.timer_duration
        self.app.query_one(PomodoroTimer).remove_class("started")
        self.pause()
        self.app.notify(pomo.alert_message)

    def update_session(self):
        pomo.toggle_state()
        self.sync_ui()

    def start(self) -> None:
        """Function to start the timer"""
        self.update_timer.resume()

    def pause(self) -> None:
        """Function to stop the timer"""
        self.update_timer.pause()

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        pomo.reset_state()
        self.sync_ui()

    def skip(self) -> None:
        """Method to move to the next session within cycle"""
        self.update_session()
        self.update_timer.resume()


class PomodoroTimer(HorizontalGroup):
    """Main Timer Widget"""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(
            TimeDisplay
        )  # query_one is like getElementById/Classname

        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "pause":
            time_display.pause()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()
        elif button_id == "skip":
            time_display.skip()

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Pause", id="pause", variant="error")
        yield Button("Reset", id="reset")
        yield Button("Skip", id="skip")
        yield TimeDisplay("00:00")


class Cycles(Static):
    def on_mount(self) -> None:
        """event handler called when a widget is added to the app"""
        self.update(f"#{pomo.lifetime_cycle_count}")

    def update_cycle(self) -> None:
        self.update(f"#{pomo.lifetime_cycle_count}")


class Current_Session(Static):
    def on_mount(self) -> None:
        """event handler called when a widget is added to the app"""
        self.update(f"{pomo.get_current_session()}")

    def update_current_session(self):
        self.update(f"{pomo.get_current_session()}")


# Turns PomodoroApp() into an async function which just allows for asyncronous code
# that couldn't be run otherwise to be run inside of it
class PomodoroApp(App):
    """A pomodoro timer cli for more productivity than you would have otherwise"""

    CSS_PATH = "./styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("s", "start", "Start"),
        ("p", "pause", "Pause"),
        ("n", "skip", "Skip"),
        ("r", "reset", "Reset"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        yield VerticalScroll(
            PomodoroTimer(),
            HorizontalGroup(Cycles(), Current_Session(), id="info-row"),
            id="main",
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_start(self) -> None:
        """An action to start the timer"""
        self.query_one(PomodoroTimer).query_one(TimeDisplay).start()
        self.query_one(PomodoroTimer).add_class("started")

    def action_pause(self) -> None:
        """An action to pause the timer"""
        self.query_one(PomodoroTimer).query_one(TimeDisplay).pause()
        self.query_one(PomodoroTimer).remove_class("started")

    def action_skip(self) -> None:
        """An action to skip the current session"""
        self.query_one(PomodoroTimer).query_one(TimeDisplay).skip()

    def action_reset(self) -> None:
        """An action to reset app state"""
        self.query_one(PomodoroTimer).query_one(TimeDisplay).reset()


def main():
    app = PomodoroApp()
    app.run()


if __name__ == "__main__":
    main()
