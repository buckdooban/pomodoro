import time


class PomodoroManager:

    def __init__(
        self,
        cycle_count=0,
        total_cycle_count=3,
        timer_duration=5,  # CHANGE BACK TO 25 FOR PRODUCTION
        time_to_focus=True,
        focus_duration=5,  # CHANGE BACK TO 25 FOR PRODUCTION
        short_break_duration=1,  # CHANGE BACK TO 5 FOR PRODUCTION
        long_break_duration=3,  # CHANGE BACK TO 15 FOR PRODUCTION
        short_break_message="Time for a short break!",
        long_break_message="Time for a long break!",
        focus_message="Time to focus!",
    ):
        self.cycle_count = cycle_count
        self.total_cycle_count = total_cycle_count
        self.timer_duration = timer_duration
        self.time_to_focus = time_to_focus
        self.FOCUS_DURATION = focus_duration
        self.SHORT_BREAK_DURATION = short_break_duration
        self.LONG_BREAK_DURATION = long_break_duration
        self.SHORT_BREAK_MESSAGE = short_break_message
        self.LONG_BREAK_MESSAGE = long_break_message
        self.FOCUS_MESSAGE = focus_message
        self.alert_message = short_break_message

    def _get_current_state(self):
        if self.cycle_count == self.total_cycle_count and not self.time_to_focus:
            return "LONG_BREAK"
        elif not self.time_to_focus:
            return "SHORT_BREAK"
        else:
            return "FOCUS"

    def toggle_state(self):
        if (
            self.cycle_count == self.total_cycle_count
            and self._get_current_state() == "LONG_BREAK"
        ):
            # print("IN toggle_state IF BLOCK")
            self.cycle_count = 0
            self.time_to_focus = True
            print(f"CYCLE COUNT: {self.cycle_count}")
            self.set_message()
            self.set_timer_duration()
        elif self.time_to_focus and self.timer_duration == self.FOCUS_DURATION:
            # print("IN toggle_state ELIF BLOCK")
            self.time_to_focus = False
            self.set_message()
            self.set_timer_duration()
            print(f"CYCLE COUNT: {self.cycle_count}")
        elif (
            not self.time_to_focus and self.timer_duration == self.SHORT_BREAK_DURATION
        ):
            # print("IN toggle_state 2nd ELIF BLOCK")
            self.time_to_focus = True
            self.cycle_count += 1
            print(f"CYCLE COUNT: {self.cycle_count}")
            self.set_message()
            self.set_timer_duration()
        else:
            print("toggle_state foobarbaz")

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

    def set_message(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            print(f"ALERT MESSAGE: {self.LONG_BREAK_MESSAGE}")
            return self.LONG_BREAK_MESSAGE
        elif current_state == "SHORT_BREAK":
            print(f"ALERT MESSAGE: {self.SHORT_BREAK_MESSAGE}")
            return self.SHORT_BREAK_MESSAGE
        else:
            print(f"ALERT MESSAGE: {self.FOCUS_MESSAGE}")
            return self.FOCUS_MESSAGE

    # async def start_timer(self):
    def start_timer(self):
        t = self.timer_duration
        state = self._get_current_state()
        print(f"\nTIMER START - {state} - TIMER LENGTH: {self.timer_duration}")
        while t:
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(f"{timer.rjust(6)}", end="\r")  # Overwrite the line each second
            # await asyncio.sleep(1)
            time.sleep(1)
            t -= 1


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
