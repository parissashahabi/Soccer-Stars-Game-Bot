import random
from environment import Environment
import math


class Chromosome:
    def __init__(self, mut_prob, recomb_prob, game_state, next_game_state, calc_fitness):
        self.parameters = []  # [player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force, force, angle]
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.fitness = 0
        self.game_state = game_state
        self.next_game_state = next_game_state
        self.calc_fitness = calc_fitness
        self.player_id = 4

        self.player_radius_min = 1
        self.player_radius_max = 60
        self.player_mass_min = 1
        self.player_mass_max = 100
        self.player_elasticity_min = 0
        self.player_elasticity_max = 1
        self.ball_radius_min = 1
        self.ball_radius_max = 30
        self.ball_mass_min = 1
        self.ball_mass_max = 100
        self.ball_elasticity_min = 0
        self.ball_elasticity_max = 1
        self.walls_thickness_min = 1
        self.walls_thickness_max = 50
        self.walls_elasticity_min = 0
        self.walls_elasticity_max = 1
        self.max_force_min = 100
        self.max_force_max = 5000
        self.force_min = 10
        self.force_max = 10000
        self.angle_min = 0
        self.angle_max = 360

        self.init_chromosome()

    def init_chromosome(self):
        player_radius = random.uniform(self.player_radius_min, self.player_radius_max)
        player_mass = random.uniform(self.player_mass_min, self.player_mass_max)
        player_elasticity = random.uniform(self.player_elasticity_min, self.player_elasticity_max)
        ball_radius = player_radius / 2
        ball_mass = random.uniform(self.ball_mass_min, self.ball_mass_max)
        ball_elasticity = random.uniform(self.ball_elasticity_min, self.ball_elasticity_max)
        walls_thickness = random.uniform(self.walls_thickness_min, self.walls_thickness_max)
        walls_elasticity = random.uniform(self.walls_elasticity_min, self.walls_elasticity_max)
        max_force = random.uniform(self.max_force_min, self.max_force_max)
        force = random.uniform(self.force_min, self.force_max)
        angle = random.uniform(self.angle_min, self.angle_max)

        # player_radius = 25
        # player_mass = 26
        # player_elasticity = 0.9
        # ball_radius = 10
        # ball_mass = 9
        # ball_elasticity = 0.9
        # walls_thickness = 20
        # walls_elasticity = 0.9
        # max_force = 1600
        # force = 8000
        # angle = 1.5

        self.parameters.append(player_radius)
        self.parameters.append(player_mass)
        self.parameters.append(player_elasticity)
        self.parameters.append(ball_radius)
        self.parameters.append(ball_mass)
        self.parameters.append(ball_elasticity)
        self.parameters.append(walls_thickness)
        self.parameters.append(walls_elasticity)
        self.parameters.append(max_force)
        self.parameters.append(force)
        self.parameters.append(angle)

        if self.calc_fitness:
            self.calculate_fitness()

    def mutation(self):

        # player_radius
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_rad = random.uniform(-2, 2)
            new_rad = self.parameters[0] + add_rad
            self.parameters[0] = min(max(self.player_radius_min, new_rad), self.player_radius_max)
            self.parameters[3] = self.parameters[0] / 2

        # player_mass
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_mass = random.uniform(-2, 2)
            new_mass = self.parameters[1] + add_mass
            self.parameters[1] = min(max(self.player_mass_min, new_mass), self.player_mass_max)
            # self.parameters[4] = self.parameters[1] / 2

        # player_elasticity
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            self.parameters[2] = random.uniform(self.player_elasticity_min, self.player_elasticity_max)

        # ball_radius
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_rad = random.uniform(-2, 2)
            new_rad = self.parameters[3] + add_rad
            self.parameters[3] = min(max(self.ball_radius_min, new_rad), self.ball_radius_max)
            self.parameters[0] = self.parameters[3] * 2

        # ball_mass
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_mass = random.uniform(-2, 2)
            new_mass = self.parameters[4] + add_mass
            self.parameters[4] = min(max(self.ball_mass_min, new_mass), self.ball_mass_max)
            # self.parameters[1] = self.parameters[4] * 2

        # ball_elasticity
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            self.parameters[5] = random.uniform(self.ball_elasticity_min, self.ball_elasticity_max)

        # walls_thickness
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_thickness = random.uniform(-2, 2)
            new_thickness = self.parameters[6] + add_thickness
            self.parameters[6] = min(max(self.walls_thickness_min, new_thickness), self.walls_thickness_max)

        # walls_elasticity
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            self.parameters[7] = random.uniform(self.walls_elasticity_min, self.walls_elasticity_max)

        # max_force
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_force = random.uniform(-50, 50)
            new_force = self.parameters[8] + add_force
            self.parameters[8] = min(max(self.max_force_min, new_force), self.max_force_max)

        # force
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_force = random.uniform(-50, 50)
            new_force = self.parameters[9] + add_force
            self.parameters[9] = min(max(self.force_min, new_force), self.force_max)

        # angle
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_deg = random.uniform(-10, 10)
            new_deg = self.parameters[10] + add_deg
            self.parameters[10] = min(max(self.angle_min, new_deg), self.angle_max)

        self.calculate_fitness()

    def calculate_fitness(self):
        player_id = self.player_id
        player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force, force, angle = self.parameters

        env = Environment(self.game_state, player_radius, player_mass, player_elasticity, ball_radius, ball_mass,
                          ball_elasticity, walls_thickness, walls_elasticity, max_force)
        env.simulate()
        Environment.shoot(env.players_shapes[player_id - 1], round(angle), round(force))
        for _ in range(500):
            env.space.step(1 / 120)

        # Get the next positions
        next_player_positions = self.next_game_state[0]
        next_opponent_positions = self.next_game_state[1]
        next_ball_position = self.next_game_state[2]

        current_player_position = env.players_shapes[player_id-1].body.position
        current_ball_position = env.soccer_ball_shape.body.position
        current_player_positions = [shape.body.position for shape in env.players_shapes]
        current_opponent_positions = [shape.body.position for shape in env.opponent_shapes]

        # Calculate error
        player_error = math.sqrt((current_player_position[0] - next_player_positions[player_id - 1][0]) ** 2 + (
                    current_player_position[1] - next_player_positions[player_id - 1][1]) ** 2)
        ball_error = math.sqrt((current_ball_position[0] - next_ball_position[0]) ** 2 + (
                    current_ball_position[1] - next_ball_position[1]) ** 2)
        players_error = sum(
            [math.sqrt((current_player_positions[i][0] - pos[0]) ** 2 + (current_player_positions[i][1] - pos[1]) ** 2)
             for i, pos in enumerate(next_player_positions)])
        opponents_error = sum([math.sqrt(
            (current_opponent_positions[i][0] - pos[0]) ** 2 + (current_opponent_positions[i][1] - pos[1]) ** 2) for
                               i, pos in enumerate(next_opponent_positions)])

        # Set fitness
        self.fitness = - ball_error - players_error - opponents_error
