class PomodoroManager:

    # initialize all of the default state, the times integers represent minutes
    # this will eventaully all be controlled from a config file but that's a later thing
    def __init__(
        self,
        current_cycle_count=1,
        total_cycle_count=4,  # cycle that long break happens on
        lifetime_cycle_count=1,
        #
        time_to_focus=True,
        timer_duration=5,  # 5 seconds
        focus_session_duration=5,  # 5 seconds
        short_break_duration=3,  # 3 seconds
        long_break_duration=8,  # 5 seconds
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
        self._alert_message = short_break_message
        self._current_session = current_session

    # single source of truth of the state of the application at any point,
    # this is where all of the functions look if they need to know what timer cycle the user is on.
    def _get_current_state(self):
        if (
            self.current_cycle_count == self.total_cycle_count
            and not self.time_to_focus
        ):
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

    @property
    def timer_duration(self):
        return self._timer_duration

    @timer_duration.setter
    def timer_duration(self, value):
        if value < 0:
            raise ValueError("Timer duration cannot be negative.")
        self._timer_duration = value

    # checks the current state of app and
    # updates timer duration accordingly
    def set_timer_duration(self):
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

    # checks the current state of app and
    # updates notification message accordingly
    def set_message(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self.alert_message = self.LONG_BREAK_MESSAGE
        elif current_state == "SHORT_BREAK":
            self.alert_message = self.SHORT_BREAK_MESSAGE
        else:
            self.alert_message = self.FOCUS_SESSION_MESSAGE

        return self.alert_message

    # @property
    # def current_session(self):
    #     return self._current_session
    #
    # # is this even necessary?
    # @current_session.setter
    # def current_session(self):
    #     return self._current_session

    def get_current_session(self):
        current_state = self._get_current_state()
        if current_state == "LONG_BREAK":
            self._current_session = "Long Break"
        elif current_state == "SHORT_BREAK":
            self._current_session = "Short Break"
        else:
            self._current_session = "Focus"

        return self._current_session
