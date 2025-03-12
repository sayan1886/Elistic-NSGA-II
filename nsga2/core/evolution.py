from tqdm import tqdm

from nsga2.core.utils import NSGA2Utils
from nsga2.core.population import Population

class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, 
                 num_of_tour_particips=2, tournament_prob=0.9, crossover_prob=0.6,
                 mutation_prob=0.1):
        self.utils = NSGA2Utils(problem=problem, 
                                num_of_individuals=num_of_individuals, 
                                num_of_tour_particips=num_of_tour_particips,
                                crossover_prob=crossover_prob, 
                                mutation_prob=mutation_prob,
                                tournament_prob=tournament_prob)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        self.population = self.utils.create_initial_population()
        self.utils.fast_non_dominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None
        for i in tqdm(range(self.num_of_generations)):
            self.population.extend(children)
            self.utils.fast_non_dominated_sort(self.population)
            new_population = Population()
            front_num = 0
            try:
                while (len(new_population) + len(self.population.fronts[front_num]) 
                    <= self.num_of_individuals):
                    self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                    new_population.extend(self.population.fronts[front_num])
                    front_num += 1

                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                self.population.fronts[front_num].sort(key=lambda individual: 
                    individual.crowding_distance, reverse=True)
                new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals 
                                                                - len(new_population)])
                returned_population = self.population
                self.population = new_population
                self.utils.fast_non_dominated_sort(self.population)
                for front in self.population.fronts:
                    self.utils.calculate_crowding_distance(front)
                children = self.utils.create_children(self.population)
                if children is None:
                    return returned_population.fronts[0]
            except IndexError:
                pass
            continue
        return returned_population.fronts[0]
