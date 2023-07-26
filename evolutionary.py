from chromosome import Chromosome
import random
from utils import calculate_k


class EvolutionaryAlgorithm:
    def __init__(self, n_iter, mut_prob, recomb_prob, population_size, min_force, max_force, game_state,radius):
        self.n_iter = n_iter
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.population = []
        self.population_size = population_size
        self.current_iter = 0
        self.fitness_avg = 0
        self.fitness_history = []
        self.max_force = max_force
        self.min_force = min_force
        self.game_state = game_state
        self.radius = radius

    # Random initialization
    def init_population(self):
        for _ in range(self.population_size):
            young_pop = Chromosome(self.mut_prob, self.recomb_prob, self.min_force, self.max_force, self.game_state, self.radius, True)
            self.population.append(young_pop)

    # Fitness Tournament selection
    def tournament_selection(self, tour_pop, k):
        parents = random.sample(tour_pop, k=k)
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        bestparent = parents[0]

        return bestparent

    def parent_selection(self):
        parents = []
        for _ in range(self.population_size):
            best_parent = self.tournament_selection(self.population,
                                                    calculate_k(len(self.population), self.current_iter, self.n_iter))
            parents.append(best_parent)

        return parents

    # One-point crossover
    def recombination(self, mating_pool):
        youngs = []
        for _ in range(self.population_size // 2):
            parents = random.choices(mating_pool, k=2)
            young_1 = Chromosome(self.mut_prob, self.recomb_prob, self.min_force, self.max_force, self.game_state, self.radius, False)
            young_2 = Chromosome(self.mut_prob, self.recomb_prob, self.min_force, self.max_force, self.game_state, self.radius, False)
            prob = random.uniform(0, 1)
            if prob <= self.recomb_prob:
                crossover_point = random.randint(1, 2)
                young_1.action = parents[0].action[:crossover_point].copy() + parents[1].action[crossover_point:].copy()
                young_2.action = parents[1].action[:crossover_point].copy() + parents[0].action[crossover_point:].copy()
            else:
                young_1.action = parents[0].action.copy()
                young_2.action = parents[1].action.copy()

            youngs.append(young_1)
            youngs.append(young_2)

        return youngs

    def survival_selection(self, youngs):
        mpl = self.population.copy() + youngs
        mpl = sorted(mpl, key=lambda agent: agent.fitness, reverse=True)
        mpl = mpl[:self.population_size].copy()

        return mpl

    def mutation(self, youngs):
        for young in youngs:
            young.mutation()

        return youngs

    def calculate_fitness_avg(self):
        self.fitness_avg = 0
        for pop in self.population:
            self.fitness_avg += pop.fitness

        self.fitness_avg /= self.population_size

    def run(self):
        self.init_population()

        for _ in range(self.n_iter):
            parents = self.parent_selection().copy()
            youngs = self.recombination(parents).copy()
            youngs = self.mutation(youngs).copy()
            self.population = self.survival_selection(youngs).copy()
            self.calculate_fitness_avg()
            self.current_iter += 1
            best_current = sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]
            print(f"current iteration: {self.current_iter} / {self.n_iter}",
                  f", best fitness: {best_current.fitness}")
            print(f'Action: {best_current.action}')
            print("-------------------------------------------------------------------------------------------------")
            self.fitness_history.append(self.fitness_avg)

            if best_current.fitness > 0:
                break

        ans = sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]
        return ans, self.fitness_history
