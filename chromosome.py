import random
from environment import Environment
from math import sqrt


class Chromosome:
    def __init__(self, mut_prob, recomb_prob, min_force, max_force, game_state, parameters, calc_fitness):
        self.action = []  # [player_id, angle, force]
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.fitness = 0
        self.max_force = max_force
        self.min_force = min_force
        self.game_state = game_state
        self.calc_fitness = calc_fitness
        self.parameters = parameters

        self.init_chromosome()

    def init_chromosome(self):
        player_id = random.randint(1, 5)
        angle = random.uniform(0, 360)
        force = random.uniform(self.min_force, self.max_force)

        self.action.append(player_id)
        self.action.append(angle)
        self.action.append(force)

        if self.calc_fitness:
            self.calculate_fitness()

    def mutation(self):
        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            self.action[0] = random.randint(1, 5)

        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_deg = random.uniform(-10, 10)
            new_deg = self.action[1] + add_deg
            self.action[1] = min(max(0, new_deg), 360)

        prob = random.uniform(0, 1)
        if prob <= self.mut_prob:
            add_force = random.uniform(-200, 200)
            new_force = self.action[2] + add_force
            self.action[2] = min(max(self.min_force, new_force), self.max_force)

        self.calculate_fitness()

    @staticmethod
    def calculate_distance_to_goal(ball_position, goal_start, goal_end):
        x, y = ball_position[0], ball_position[1]
        x1, y1 = goal_start[0], goal_start[1]
        x2, y2 = goal_end[0], goal_end[1]

        distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / sqrt((y2 - y1)**2 + (x2 - x1)**2)

        return distance

    def calculate_fitness(self):
        player_id, angle, force = self.action[0], self.action[1], self.action[2]
        player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force, _, _ = self.parameters
        env = Environment(self.game_state, player_radius, player_mass, player_elasticity, ball_radius, ball_mass, ball_elasticity, walls_thickness, walls_elasticity, max_force)
        env.simulate()
        Environment.shoot(env.players_shapes[player_id-1], round(angle), round(force))
        for _ in range(500):
            env.space.step(1 / 120)

        if env.check_player_goal_scored() is True:
            self.fitness = 100
        elif env.check_opponent_goal_scored() is True:
            self.fitness = -10000  # Very low value for opponent's goal
        else:
            ball_position = env.soccer_ball_shape.body.position
            opponent_goal_start = (env.opponent_goal_position[0], env.opponent_goal_position[1])
            opponent_goal_end = (env.opponent_goal_position[0], env.opponent_goal_position[1] - env.opponent_goal_position[3])

            distance_to_goal = Chromosome.calculate_distance_to_goal(ball_position, opponent_goal_start, opponent_goal_end)
            self.fitness = -distance_to_goal
