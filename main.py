import asyncio
import pomoclass
import signal
import sys
from desktop_notifier import DesktopNotifier, Button

pomo = pomoclass.PomodoroManager()


async def main():
    # defines asyncio events to act as booleans for timer events
    start_event = asyncio.Event()
    stop_event = asyncio.Event()
    pause_event = asyncio.Event()
    skip_event = asyncio.Event()
    reset_event = asyncio.Event()
    user_ready_event = asyncio.Event()

    background_tasks = set()

    # Shut down sequence - let the user quit the program if it's running
    def shut_it_down():
        stop_event.set()
        user_ready_event.set()

    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGINT, shut_it_down)
    loop.add_signal_handler(signal.SIGTERM, shut_it_down)

    # creates a way to listen for user input while timer is running
    async def get_user_input():
        while not stop_event.is_set():

            # creates a seperate thread that listens for user input
            # while the timer is running
            user_input = await asyncio.to_thread(sys.stdin.readline)
            command = user_input.strip().lower()

            if command == "start":
                start_event.set()
            elif command == "stop":
                stop_event.set()
            elif command == "skip":
                skip_event.set()
            elif command == "pause":
                pause_event.set()
            elif command == "reset":
                reset_event.set()

    #
    task = asyncio.create_task(get_user_input())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    notifier = DesktopNotifier(app_name="Pomodoro Timer CLI")

    # run the timer and send notifications to the user until a stop event is triggered
    while not stop_event.is_set():

        await pomo.handle_timer(
            start_event, stop_event, pause_event, skip_event, reset_event
        )

        if stop_event.is_set():
            break

        pomo.toggle_state()

        await notifier.send(
            title="Pomodoro Timer",
            message=f"{pomo.alert_message} - cycle: {pomo.lifetime_cycle_count + 1}",
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
