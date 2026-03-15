import pomoclass

pomo = pomoclass.PomodoroManager()

while pomo.cycle_count <= pomo.total_cycle_count:
    pomo.start_timer()
    pomo.toggle_state()
