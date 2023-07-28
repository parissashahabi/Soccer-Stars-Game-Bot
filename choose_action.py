from evolutionary import EvolutionaryAlgorithm
import numpy as np
import sys


class ChooseAction:
    def __init__(self, N_iter, population_size, mut_prob, recomb_prob, min_force, max_force, game_state, radius):
        self.N_iter = N_iter  # 50
        self.population_size = population_size  # 50
        self.mut_prob = mut_prob  # 0.9
        self.recomb_prob = recomb_prob  # 0.5
        self.min_force = min_force  # 10
        self.max_force = max_force  # 10000
        self.game_state = game_state
        self.radius = radius
        self.history = None
        self.best_action = None

    def search(self):
        ea = EvolutionaryAlgorithm(self.N_iter, self.mut_prob, self.recomb_prob, self.population_size, self.min_force,
                                   self.max_force, self.game_state, self.radius)
        self.best_action, self.history = ea.run()
        np.savetxt("history.csv", self.history, delimiter=",")

    def save_action(self, count):
        original_stdout = sys.stdout
        with open(f'action reports/action_report{count}.txt', 'w') as f:
            sys.stdout = f
            print(f"Game State: {self.game_state}")
            print(f"Fitness: {self.best_action.fitness}")
            print(f"Player Id: {self.best_action.action[0]}")
            print(f"Angle: {self.best_action.action[1]}")
            print(f"Force: {self.best_action.action[2]}")
            sys.stdout = original_stdout


# state = ([(267, 243), (422, 318), (147, 363), (421, 411), (269, 487)], [(792, 240), (606, 363), (884, 363), (699, 365), (790, 487)], (512.4279937744141, 368.6336669921875), (58, 259, 60, 201), (917, 258, 48, 200), (116, 142, 797, 461))
# ca = ChooseAction(50, 80, 0.9, 0.5, 10, 10000, state, 20)
# ca.search()
# ca.save_action(1)
