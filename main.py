import asyncio
import pomoclass
import signal
import sys
import os
from desktop_notifier import DesktopNotifier, Button

pomo = pomoclass.PomodoroManager()


# Turns main() into an async function which just allows for asyncronous code
# that couldn't be run otherwise to be run inside of it
async def main():
    # defines asyncio events to act as booleans for timer events
    start_event = asyncio.Event()
    stop_event = asyncio.Event()
    pause_event = asyncio.Event()
    skip_event = asyncio.Event()
    reset_event = asyncio.Event()
    user_ready_event = asyncio.Event()

    # sometimes, the Python garbage collector will clean up any background asyncio.Task() objects that aren't explicitly held in memory
    # so the asyncio docs recommend putting any process that isn't a function or saved to a variable in a set()
    # I do this with get_user_input() (which reads cli commands, not notification events)
    # since it could theoretically run in the background for hours
    background_tasks = set()

    # Shut down sequence - let the user quit the program if it's running
    def shut_it_down():
        stop_event.set()
        user_ready_event.set()
        print("\nShutting down...")
        os._exit(0)

    # get_running_loop() is a method that lets you hook into the event loop that runs
    # whenever you're in an async function
    loop = asyncio.get_running_loop()

    # triggers shut_it_down() when the user types ctrl+c or kill into their terminal
    loop.add_signal_handler(signal.SIGINT, shut_it_down)
    loop.add_signal_handler(signal.SIGTERM, shut_it_down)

    # creates a way to listen for user input while timer is running
    async def get_user_input():
        while not stop_event.is_set():

            # creates a seperate thread that runs in the background and listens for user input while the timer is running
            user_input = await asyncio.to_thread(sys.stdin.readline)
            command = user_input.strip().lower()

            if command == "start":
                start_event.set()
            elif command in ["stop", "exit", "quit", ":q"]:
                stop_event.set()
            elif command == "skip":
                skip_event.set()
            elif command == "pause":
                pause_event.set()
            elif command == "reset":
                reset_event.set()

    # this is the other piece of that garbage collection failsafe that I mentioned above
    # this is where get_user_input() is added as a background task so Python doesn't garbage collect it
    task = asyncio.create_task(get_user_input())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    # gets an instance of the DesktopNotifier object so I can send the notification to the window
    # and response to user click events
    notifier = DesktopNotifier(app_name="Pomodoro Timer CLI")

    # run the timer and send notifications to the user until a stop event is triggered
    while not stop_event.is_set():

        # calls the function that controls the timer and sends user input events to it so it can respond in kind
        await pomo.handle_timer(
            start_event, stop_event, pause_event, skip_event, reset_event
        )

        if stop_event.is_set():
            break

        pomo.toggle_state()

        # this is the notification and the buttons
        await notifier.send(
            title="Pomodoro Timer",
            message=f"{pomo.alert_message}",
            buttons=[Button(title="Dismiss", on_pressed=user_ready_event.set)],
            # on_dispatched=lambda: print("Notification showing"),
            on_clicked=user_ready_event.set,
            on_dismissed=user_ready_event.set,
        )

        # pauses the timer loop until the user is ready for it to continue
        # aka: the notification button is pressed
        await user_ready_event.wait()
        user_ready_event.clear()


if __name__ == "__main__":
    asyncio.run(main())
