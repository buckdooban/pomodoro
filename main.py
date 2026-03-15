import asyncio
import pomoclass
import signal
from desktop_notifier import DesktopNotifier, Button

pomo = pomoclass.PomodoroManager()


async def main():
    stop_event = asyncio.Event()
    user_ready_event = asyncio.Event()

    def shut_it_down():
        stop_event.set()
        user_ready_event.set()

    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGINT, shut_it_down)
    loop.add_signal_handler(signal.SIGTERM, shut_it_down)

    notifier = DesktopNotifier(app_name="Pomodoro Timer CLI")

    while not stop_event.is_set():
        await pomo.start_timer(stop_event)
        pomo.toggle_state()

        await notifier.send(
            title="Pomodoro Timer",
            message=f"{pomo.alert_message} - cycle: {pomo.cycle_count}",
            buttons=[Button(title="Dismiss", on_pressed=user_ready_event.set)],
            # on_dispatched=lambda: print("Notification showing"),
            on_clicked=user_ready_event.set,
            on_dismissed=shut_it_down,
        )

        await user_ready_event.wait()
        user_ready_event.clear()


if __name__ == "__main__":
    asyncio.run(main())
