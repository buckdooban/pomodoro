class PomodoroManager:

    def __init__(
        self,
        current_cycle_count=1,
        total_cycle_count=4,  # cycle that long break happens on
        lifetime_cycle_count=1,
        #
        time_to_focus=True,
        timer_duration=1500,  # 25 minutes
        focus_session_duration=1500,  # 25 minutes
        short_break_duration=300,  # 5 minutes
        long_break_duration=900,  # 15 minutes
        #
        short_break_message="Time for a short break!",
        long_break_message="Time for a long break!",
        focus_session_message="Time to focus!",
        current_session="Focus",
    ):
        self.current_cycle_count = current_cycle_count
        self.total_cycle_count = total_cycle_count
        self.lifetime_cycle_count = lifetime_cycle_count
        #
        self.time_to_focus = time_to_focus
        self._timer_duration = timer_duration
        self.FOCUS_SESSION_DURATION = focus_session_duration
        self.SHORT_BREAK_DURATION = short_break_duration
        self.LONG_BREAK_DURATION = long_break_duration
        #
        self.SHORT_BREAK_MESSAGE = short_break_message
        self.LONG_BREAK_MESSAGE = long_break_message
        self.FOCUS_SESSION_MESSAGE = focus_session_message
        self.alert_message = short_break_message
        self._current_session = current_session

    def _get_current_state(self):
        """Source of truth for where the state of the app is
        at any given point. Focus, short break, long break"""
        if (
            self.current_cycle_count == self.total_cycle_count
            and not self.time_to_focus
        ):
            return "LONG_BREAK"
        elif not self.time_to_focus:
            return "SHORT_BREAK"
        else:
            return "FOCUS"

    def toggle_state(self):
        if self.time_to_focus:
            self.time_to_focus = False
        else:
            # Break just ended, decide if we reset or increment
            if self.current_cycle_count == self.total_cycle_count:
                self.current_cycle_count = 0
                self.lifetime_cycle_count += 1
            else:
                self.current_cycle_count += 1
                self.lifetime_cycle_count += 1
            self.time_to_focus = True

        # after state updates, fire off correct message and
        # set appropriate timer duration based on the state
        self.set_message()
        self.set_timer_duration()

    def reset_state(self):
        self.current_cycle_count = 1
        self.total_cycle_count = 4
        self.lifetime_cycle_count = 1
        self.time_to_focus = True
        self.timer_duration = 5
        self.focus_session_duration = 5
        self.short_break_duration = 3
        self.long_break_duration = 8
        self.short_break_message = "Time for a short break!"
        self.long_break_message = "Time for a long break!"
        self.focus_session_message = "Time to focus!"
        self.current_session = "Focus"
        self.set_message()

    @property
    def timer_duration(self):
        return self._timer_duration

    @timer_duration.setter
    def timer_duration(self, value):
        if value < 0:
            raise ValueError("Timer duration cannot be negative.")
        self._timer_duration = value

    def set_timer_duration(self):
        """checks the current state of app and
        updates timer duration accordingly"""

        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self._timer_duration = self.LONG_BREAK_DURATION
            return self.timer_duration
        elif current_state == "SHORT_BREAK":
            self._timer_duration = self.SHORT_BREAK_DURATION
            return self._timer_duration
        elif current_state == "FOCUS":
            self._timer_duration = self.FOCUS_SESSION_DURATION
            return self._timer_duration
        else:
            print("set_timer_duration foobarbaz")

    def set_message(self):
        """checks the current state of app and
        updates notification message accordingly"""

        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self.alert_message = self.LONG_BREAK_MESSAGE
        elif current_state == "SHORT_BREAK":
            self.alert_message = self.SHORT_BREAK_MESSAGE
        else:
            self.alert_message = self.FOCUS_SESSION_MESSAGE

        return self.alert_message

    def get_current_session(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self._current_session = "Long Break"
        elif current_state == "SHORT_BREAK":
            self._current_session = "Short Break"
        else:
            self._current_session = "Focus"

        return self._current_session
