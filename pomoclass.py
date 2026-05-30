import asyncio

# BUG:  total_cycle_count should always increment after a break has ended, currently only incrementing after short breaks
# TODO: refactor currrent classes to use decorators
# TODO: walk through Textual tutorial in a different repo
# TODO: get familiar with TOML and what is controlled with the pyproject.toml file


class PomodoroManager:

    # initialize all of the default state, the times integers represent minutes
    # this will eventaully all be controlled from a config file but that's a later thing
    def __init__(
        self,
        cycle_count=0,
        total_cycle_count=3,
        lifetime_cycle_count=0,
        # timer_duration=1500,  # 25 minutes - how long the timer is at any given moment
        timer_duration=3,  # 5 seconds
        time_to_focus=True,
        # focus_duration=1500,  # 25 minutes - how long a "focus cycle" is
        focus_duration=3,  # 5 seconds
        # short_break_duration=300,  # 5 minutes
        # long_break_duration=900,  # 15 minutes
        short_break_duration=1,  # 3 seconds
        long_break_duration=5,  # 5 seconds
        short_break_message="Time for a short break!",
        long_break_message="Time for a long break!",
        focus_message="Time to focus!",
    ):
        self.cycle_count = cycle_count
        self.total_cycle_count = total_cycle_count
        self.lifetime_cycle_count = lifetime_cycle_count
        self.timer_duration = timer_duration
        self.time_to_focus = time_to_focus
        self.FOCUS_DURATION = focus_duration
        self.SHORT_BREAK_DURATION = short_break_duration
        self.LONG_BREAK_DURATION = long_break_duration
        self.SHORT_BREAK_MESSAGE = short_break_message
        self.LONG_BREAK_MESSAGE = long_break_message
        self.FOCUS_MESSAGE = focus_message
        self.alert_message = short_break_message

    # single source of truth of the state of the application at any point,
    # this is where all of the functions look if they need to know what timer cycle the user is on.
    def _get_current_state(self):
        if self.cycle_count == self.total_cycle_count and not self.time_to_focus:
            return "LONG_BREAK"
        elif not self.time_to_focus:
            return "SHORT_BREAK"
        else:
            return "FOCUS"

    # updates state after every timer sequence
    # i.e. when a focus session ends, when a short or a long break ends
    def toggle_state(self):
        # if the timer goes off and it's time to focus, a break just ended
        # switch time_to_focus to false so the next time a timer ends the
        # app knows it's time for a break
        if self.time_to_focus:
            self.time_to_focus = False
        else:
            # Break just ended, decide if we reset or increment
            if self.cycle_count == self.total_cycle_count:
                self.cycle_count = 0
            else:
                self.cycle_count += 1
                self.lifetime_cycle_count += 1
            self.time_to_focus = True

        # after state updates, fire off correct message and
        # set appropriate timer duration based on the state
        self.set_message()
        self.set_timer_duration()

    # checks the current state of app and
    # updates timer duration accordingly
    def set_timer_duration(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self.timer_duration = self.LONG_BREAK_DURATION
            return self.timer_duration
        elif current_state == "SHORT_BREAK":
            self.timer_duration = self.SHORT_BREAK_DURATION
            return self.timer_duration
        elif current_state == "FOCUS":
            self.timer_duration = self.FOCUS_DURATION
            return self.timer_duration
        else:
            print("set_timer_duration foobarbaz")

    # checks the current state of app and
    # updates notification message accordingly
    def set_message(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self.alert_message = self.LONG_BREAK_MESSAGE
        elif current_state == "SHORT_BREAK":
            self.alert_message = self.SHORT_BREAK_MESSAGE
        else:
            self.alert_message = self.FOCUS_MESSAGE

        print(f"total cycle count: {self.lifetime_cycle_count}")
        return self.alert_message

    # starts countdown at app start, reacts to user input
    async def handle_timer(
        self, start_event, stop_event, pause_event, skip_event, reset_event
    ):
        t = self.timer_duration
        print("\nTimer started")
        while t > 0 and not stop_event.is_set():
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(
                f"{timer.rjust(6)}", end="\r"
            )  # Overwrite the line each second (the majority of the countdown code was stoken from a geeksforgeeks article linked below)
            # gives up control flow once a second so that user input can be checked for
            await asyncio.sleep(1)

            # check for asyncio.Flags raised
            if pause_event.is_set():
                print("Timer paused.")

                # fixes a bug where i couldn't quit while timer was paused
                # i had to start the timer back up before i could quit
                # this basically tells the event loop "if the timer is paused,
                # watch for both a start_event and a stop_event and go with whichever finished first"
                wait_start = asyncio.create_task(start_event.wait())
                wait_stop = asyncio.create_task(stop_event.wait())

                await asyncio.wait(
                    [wait_start, wait_stop], return_when=asyncio.FIRST_COMPLETED
                )

                pause_event.clear()
                start_event.clear()
            elif stop_event.is_set():
                print("\nShutting down...")
                break
            elif start_event.is_set():
                print("\nRestarting timer")
            elif reset_event.is_set():
                print(
                    "\nreset_event flag is set, reseting timer sequence and app state back to default values"
                )
                self.cycle_count = 0
                self.lifetime_cycle_count = 0
                self.time_to_focus = True
                self.set_timer_duration()
                self.set_message()
                t = self.timer_duration
                reset_event.clear()
            elif skip_event.is_set():
                print("\nskipped to next cycle sequence early.")
                skip_event.clear()
                break
            t -= 1
            ###
            # https://www.geeksforgeeks.org/python/how-to-create-a-countdown-timer-using-python/
            ###

        # fixes bug where the timer wouldn't go all the way down to 00:00
        if t == 0 and not skip_event.is_set() and not stop_event.is_set():
            print(" 00:00", end="\r\n")


###
# CYCLE LOGIC FLOW
###

# CYCLE ONE
#
# cycle_count = 0
# time_to_focus = True
# timer_duration = 25
# <timer goes off>
# toggle_state()
#
# cycle_count = 0
# time_to_focus = False
# timer_duration = 5
# <timer goes off>
# toggle_state()
#
# CYCLE TWO
#
# cycle_count = 1
# time_to_focus = True
# timer_duration = 25
# toggle_state()
#
# cycle_count = 1
# time_to_focus = False
# timer_duration = 5
# toggle_state()
#
# CYCLE THREE
#
# cycle_count = 2
# time_to_focus = True
# timer_duration = 25
# toggle_state()
#
# cycle_count = 2
# time_to_focus = False
# timer_duration = 5
# toggle_state()
#
# CYCLE FOUR
#
# cycle_count = 3
# time_to_focus = True
# timer_duration = 25
# toggle_state()
#
# cycle_count = 3
# time_to_focus = False
# timer_duration = 15
# toggle_state()
