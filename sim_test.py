from environment import Environment

count = 2
with open(f'simulation/simulation_report_{count}.txt', 'r') as file:
    lines = file.readlines()

state_str = lines[0].split(": ")[1].strip()
next_state_str = lines[1].split(": ")[1].strip()
player_id = int(lines[2].split(": ")[1].strip())
fitness = float(lines[3].split(": ")[1].strip())
parameters_str = lines[4].split(": ")[1].strip().replace('[', '').replace(']', '')
parameters = list(map(float, parameters_str.split(", ")))

state = eval(state_str)

player_positions, opponent_positions, ball_position, player_goal, opponent_goal, _ = state

player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force, force, angle = parameters

env = Environment(state, player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force)
env.simulate()
env.visualize(player_id - 1, angle, force)


