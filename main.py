import pomoclass

# from desktop_notifier import DesktopNotifier, Button

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Static

pomo = pomoclass.PomodoroManager()

# BUG:  cycle_count should always increment after next focus session has started,
# currently incrementing once short break has ended
# TODO: create display fields that show if user is in focus, short break, or long break
# TODO: implement logic or skipping breaks/ focus sessions
# TODO: create key bindings for:
# start, stop, reset, skip
# TODO: refactor the rest of the classes in PomodoroManager to use decorators
# TODO: rename classes in main.py to reflect naming associated with a timer and not a stopwatch
# TODO: Style app to look a little nicer
# TODO: get familiar with TOML and what is controlled with the pyproject.toml file
# TODO: see if there is a replacement for if you can get DesktopNotifier to work for system-level notifications
# TODO: See if you can make sound happen at the end of sessions
# TODO: Update README.md
# INFO: The app can be suspended with `ctrl + z` like normal but you can also bind a "suspend" event to a key and have Textual run system code like starting the default terminal app to give the user their terminal back once they've started the timer


class TimeDisplay(Digits):
    """Widget displaying timer face"""

    timer_duration = pomo.timer_duration
    focus_duration = pomo.FOCUS_SESSION_DURATION

    start_time = timer_duration
    time = reactive(timer_duration)
    total = reactive(timer_duration)

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
            # update cycle count in UI
            self.app.query_one(Cycles).update_cycle()
            # update current session in UI
            self.app.query_one(Current_Session).update_current_session()
            self.update(f"{mins:02.0f}:{secs:05.2f}")
            pomo.toggle_state()
            self.app.notify(pomo.alert_message)
            self.time = pomo.timer_duration
            self.stop()
            self.app.query_one(Stopwatch).remove_class("started")
        else:
            self.update(f"{mins:02.0f}:{secs:05.2f}")

    def start(self) -> None:
        """Function to start the timer"""
        self.update_timer.resume()

    def stop(self) -> None:
        """Function to stop the timer"""
        self.update_timer.pause()

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = self.focus_duration
        self.time = self.focus_duration


class Stopwatch(HorizontalGroup):
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
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00")


class Cycles(Static):
    DEFAULT_CSS = """
    Cycles {
        width: 25;
        height: 5;
        padding: 1 2;
        background: $panel;
        border: $secondary tall;
        content-align: center middle;
    }
    """

    def on_mount(self) -> None:
        """event handler called when a widget is added to the app"""
        self.update(f"#{pomo.current_cycle_count}")

    def update_cycle(self) -> None:
        self.update(f"#{pomo.current_cycle_count}")


class Current_Session(Static):
    DEFAULT_CSS = """
    Current_Session {
        width: 25;
        height: 5;
        padding: 1 2;
        background: $panel;
        border: $secondary tall;
        content-align: center middle;
    }
    """

    def on_mount(self) -> None:
        """event handler called when a widget is added to the app"""
        self.update(f"{pomo.get_current_session()}")

    def update_current_session(self):
        self.update(f"{pomo.get_current_session()}")


# Turns main() into an async function which just allows for asyncronous code
# that couldn't be run otherwise to be run inside of it
class StopwatchApp(App):
    """A pomodoro timer cli for more productivity than you would have otherwise"""

    CSS_PATH = "./styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), Cycles(), Current_Session())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
