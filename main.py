import asyncio
import signal
from desktop_notifier import DesktopNotifier, Urgency, Button, DEFAULT_SOUND

# MVP constants
POMODORO_CYCLE = ("Pomodoro", 5)
SHORT_BREAK = ("Short", 1)
LONG_BREAK = ("Long", 3)

# dictionary
state = {
    "current_cycle": {
        "POMODORO_CYCLE": POMODORO_CYCLE,
        "SHORT_BREAK": SHORT_BREAK,
        "LONG_BREAK": LONG_BREAK,
    },
    "short_break": True,
}

time_for_short_break = "Short" if state["short_break"] else "Long"


async def main():

    def countdown():
        print("timer started")
        # while t:
        #     mins, secs = divmod(t, 60)
        #     timer = "{:02d}:{:02d}".format(mins, secs)
        #     print(f"{timer.rjust(6)}", end="\r")  # Overwrite the line each second
        #     time.sleep(1)
        #     t -= 1
        print("Fire in the hole!!")

    notifier = DesktopNotifier(app_name="Pomodoro Timer")

    await notifier.send(
        # """
        # This function listens for the timer to be over
        # Accepts user input, fires appropriate callback function and adjusts state
        # """
        title=f"{state['current_cycle']['POMODORO_CYCLE'][0]} cycle over",
        message=f"Time for a {time_for_short_break} break",
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title="Start Break",
                on_pressed=lambda: print("Break started"),
            ),
            Button(
                title="Reset Timer",
                on_pressed=lambda: print("Timer reset"),
            ),
        ],
        on_dispatched=lambda: countdown(),
        on_clicked=lambda: print("Notification clicked"),
        on_dismissed=lambda: print("Notification dismissed"),
        sound=DEFAULT_SOUND,
    )

    # Run the event loop forever to respond to user interactions with the notification.
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    # break conditions
    # SIGINT listens for ctl+c, SIGTERM listens for a termination signal
    # without these here the program wouldn't stop
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)

    await stop_event.wait()


asyncio.run(main())
