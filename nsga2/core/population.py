class Population:

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()
    
    def copy(self):
        new_copy = Population()
        new_copy.population = self.population.copy()
        new_copy.fronts = self.fronts.copy()
        return new_copy

    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def append(self, new_individual):
        self.population.append(new_individual)
        
    def remove(self, individual):
        self.population.remove(individual)
    
    def unique_population(self):
        return set(self.population)
