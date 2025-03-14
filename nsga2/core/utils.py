import random

from .population import Population

class NSGA2Utils:

    def __init__(self, problem, num_of_individuals=100,
                 num_of_tour_particips=2, crossover_prob=0.6, mutation_prob=0.1,
                 tournament_prob=0.9):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.tournament_prob = tournament_prob

    def create_initial_population(self):
        population = Population()
        while self.num_of_individuals != len(population):
            individual = self.problem.generate_individual()
            self.problem.calculate_objectives(individual)
            if individual.is_unique(population.population):
                population.append(individual)
        return population

    def fast_non_dominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10 ** 9
                front[solutions_num - 1].crowding_distance = 10 ** 9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: 
                    scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (front[i + 1].objectives[m] - 
                                                   front[i - 1].objectives[m]) / scale

    def crowding_operator(self, individual, other_individual):
        if individual.rank is None or other_individual.rank is None:
            return 1
        elif individual.rank is None:
            return -1
        elif other_individual.rank is None:
            return 1
        elif (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > 
                        other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1, parent2 = self.__selection(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        child1 = individual1
        child2 = individual2
        if (self.__choose_with_prob(self.crossover_prob)):
            child1, child2 = individual1.crossover(individual2)            
        return child1, child2

    def __mutate(self, child):
        if (self.__choose_with_prob(self.mutation_prob)):
            child.mutate()
            
    def __selection(self, population):
        parent1 = self.__tournament(population)
        parent2 = parent1
        retries = 0
        while parent1 == parent2 and retries <= 5:
            parent2 = self.__tournament(population)
            retries += 1
        return parent1, parent2
    
    def __tournament(self, population):
        unique_population = list(population.unique_population())
        if len(unique_population) < self.num_of_tour_particips:
            return unique_population[0]
        participants = random.sample(unique_population, self.num_of_tour_particips)
        best = None
        for participant  in participants:
            if best is None or (
                    self.crowding_operator(participant, best) == 1 and 
                    self.__choose_with_prob(self.tournament_prob)):
                best = participant
        return best

    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False
