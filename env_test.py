from environment import Environment
import time
with open('action reports/action_report1.txt', 'r') as file:
    lines = file.readlines()

state_str = lines[0].split(': ')[1].strip()
state = eval(state_str)

fitness = int(lines[1].split(': ')[1].strip())
player_id = int(lines[2].split(': ')[1].strip()) - 1
angle = float(lines[3].split(': ')[1].strip())
force = float(lines[4].split(': ')[1].strip())

start_time = time.time()

e = Environment(state, 20)
e.simulate()
e.visualize(player_id, angle, force)
# w, h = e.playground[2] + 2 * e.playground[0], e.playground[3] + 2 * e.playground[1]
# Environment.capture_screenshot(e.space, w, h, "images/env.png")

# ----------------------------------------------------------------------------------------------------
print("Position Before Shot: ", tuple(e.players_shapes[player_id].body.position))
Environment.shoot(e.players_shapes[player_id], angle, force)
for _ in range(500):
    e.space.step(1/120)

end_time = time.time()
duration_ms = (end_time - start_time) * 1000
print("Simulation Duration: {:.2f} milliseconds".format(duration_ms))
print("Position After Shot: ", tuple(e.players_shapes[player_id].body.position))
print("Stop: ", e.check_objects_stopped())
print("Player Goal: ", e.check_player_goal_scored())
print("Opponent Goal: ", e.check_opponent_goal_scored())
