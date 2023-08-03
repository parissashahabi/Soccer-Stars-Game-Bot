from sim_evolutionary import EvolutionaryAlgorithm
import numpy as np
import sys


class Simulate:
    def __init__(self, N_iter, population_size, mut_prob, recomb_prob, game_state, next_game_state):
        self.N_iter = N_iter  # 50
        self.population_size = population_size  # 50
        self.mut_prob = mut_prob  # 0.9
        self.recomb_prob = recomb_prob  # 0.5
        self.game_state = game_state
        self.next_game_state = next_game_state
        self.history = None
        self.best_action = None

    def search(self):
        ea = EvolutionaryAlgorithm(self.N_iter, self.mut_prob, self.recomb_prob, self.population_size, self.game_state, self.next_game_state)
        self.best_action, self.history = ea.run()
        np.savetxt("simulation/history.csv", self.history, delimiter=",")

    def save_parameters(self, count):
        original_stdout = sys.stdout
        with open(f'simulation/simulation_report_{count}.txt', 'w') as f:
            sys.stdout = f
            print(f"Game State: {self.game_state}")
            print(f"Next Game State: {self.next_game_state}")
            print(f"Player Id: {self.best_action.player_id}")
            print(f"Fitness: {self.best_action.fitness}")
            print(f"Parameters: {self.best_action.parameters}")
            sys.stdout = original_stdout


state = ([(240, 247), (210, 346), (148, 361), (298, 407), (242, 494)], [(789, 243), (429, 273), (881, 366), (697, 367), (704, 487)], (676.8642272949219, 422.5126495361328), (58, 261, 60, 201), (917, 259, 48, 200), (116, 143, 797, 461))
next_state = ([(240, 247), (210, 346), (148, 361), (756, 435), (242, 494)], [(789, 243), (429, 273), (881, 366), (853, 264), (704, 487)], (783.9066162109375, 580.4228515625), (58, 261, 60, 201), (917, 259, 48, 200), (116, 143, 797, 461))

sim = Simulate(500, 800, 0.9, 0.3, state, next_state)
sim.search()
sim.save_parameters(3)
