import asyncio


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
        if self.time_to_focus:
            # Focus just ended, always switch to break
            self.time_to_focus = False
        else:
            # Break just ended, decide if we reset or increment
            if self.cycle_count == self.total_cycle_count:
                self.cycle_count = 0
            else:
                self.cycle_count += 1
            self.time_to_focus = True

        # After the variables are updated, sync the message and timer
        self.set_message()
        self.set_timer_duration()

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
            self.alert_message = self.LONG_BREAK_MESSAGE
        elif current_state == "SHORT_BREAK":
            self.alert_message = self.SHORT_BREAK_MESSAGE
        else:
            self.alert_message = self.FOCUS_MESSAGE

        # print(f"ALERT MESSAGE: {self.alert_message}")
        return self.alert_message

    async def start_timer(self, stop_event):
        t = self.timer_duration
        state = self._get_current_state()
        print(f"\nTIMER START - {state} - TIMER LENGTH: {self.timer_duration}")
        while t and not stop_event.is_set():
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(f"{timer.rjust(6)}", end="\r")  # Overwrite the line each second
            await asyncio.sleep(1)
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
