from .individual import Individual

class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, 
                 expand=True, same_range=False, n_chromosome=8):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.expand = expand
        self.variables_range = []
        self.n_chromosome = n_chromosome
        self.n_gene = num_of_variables
        self.chromosome = None
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range

    def generate_individual(self):
        individual = Individual(self.variables_range, self.n_chromosome, self.n_gene)
        return individual

    def calculate_objectives(self, individual):
        if self.expand:
            individual.objectives = [f(*individual.features()) for f in self.objectives]
        else:
            individual.objectives = [f(individual.features()) for f in self.objectives]
