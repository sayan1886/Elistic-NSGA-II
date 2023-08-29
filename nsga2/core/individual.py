import random

class Individual(object):

    def __init__(self, variables_range, n_chromosome=8, n_gene=1, chromosome = None,
                 crossover_type="single", mutation_type="bit_swap"):
        self.variables_range = variables_range
        self.n_chromosome = n_chromosome
        self.n_gene = n_gene
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        # self.features = None
        self.objectives = None
        if chromosome is None:
            chromosome = self.__generate_random_chromosome()
        self.chromosome = chromosome.copy()
        

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features() == other.features()
        return False
    
     # genarate a randome chromosome with number of gene
    def __generate_random_chromosome(self):
        chromosome = [0] * self.n_gene
        for i in range(self.n_gene):
            chromosome[i] = self.__generate_random_gene().copy()
        return chromosome
    
    # genarate a randome gene main unit of chromosome
    def __generate_random_gene(self):
        gene = [0] * self.n_chromosome
        for i in range(self.n_chromosome):
            gene[i] = random.randint(0,1)
        return gene
    
    # encode chromosome will return array of integer 
    # where each integer denote a enocded gene
    def __encode_chromosome(self):
        # array of integer represent encoded genes 
        # converted from binary string array or gene
        encoded_chromosome = [0] * self.n_gene
        for i in range(self.n_gene):
            encoded_chromosome[i] = self.__encode_gene(self.chromosome[i])
        return encoded_chromosome
    
    # encode gene(binary string array) to integer value
    def __encode_gene(self, gene):
        # convert binary list to string
        binary_string = ''.join(map(str, gene))
        # convert binary string to integer
        encoded_gene = int(binary_string, 2) 
        return encoded_gene
    
    # evaluate corresponding chormosome value 
    def __corresponding_value(self):
        # array of integer represent encoded genes
        encoded_chromosome = self.__encode_chromosome()
        corresponding_value = [0] * self.n_gene
        for i in range(self.n_gene):
            corresponding_value[i] = self.__corresponding_gene_value(
                                        encoded_chromosome[i])
        return corresponding_value
    
    # calcualate corresponfing gene value using interpolation
    # where y_min = config.bounday.min y_max = config.bounday.min
    # x_max = 2^chormosomeLength - 1 and x_min = 0
    # x will encoded gene value
    # y = y_min + (y_max - y_min) / (x_max - x_min) * (x - x_min)
    def __corresponding_gene_value(self, encoded_gene):
        # y = self.__get_y()
        y_min = self.variables_range[0][0]
        y_max = self.variables_range[0][1]
        corresponding_value = (y_min + 
                        ((y_max - y_min) / 
                        (2 ** self.n_chromosome - 1) - 0) * 
                        (encoded_gene - 0))
        return corresponding_value
    
    # TODO: need to add variable range y 
    def __get_y(self, gene_index):
        y = self.variables_range[0]
        if(len(self.variables_range)) > 1:
            y = self.variables_range[gene_index] 
        return y
    
    def features(self):
        return self.__corresponding_value()

    # get dominace relationship
    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and abs(first) <= abs(second)
            or_condition = or_condition or abs(first) < abs(second)
        return (and_condition and or_condition)
    
    # produce a new offspring from 2 parents
    def crossover(self, other):
        offspring = None
        if (self.crossover_type == "single"):
            offspring = self.__single_point_crossover(other)
        elif (self.crossover_type == "uniform"):
            offspring = self.__uniform_crossover(other)
        else:
            print("invalid crossover type")
            exit()
        return offspring
    
    # cross over to creat one offspring from two parents 
    # using single point crossover return new offspring(s) 
    # will consider to breed single offspring gene from parent gene
    def __single_point_crossover(self, other):
        offspring_1 = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring_1[i] = self.__single_point_gene_crossover(
                self_gene=self.chromosome[i], other_gene=other.chromosome[i])
        return Individual(self.variables_range, self.n_chromosome, self.n_gene, 
                          offspring_1, self.crossover_type, self.mutation_type) 
    
    # crossover to creat one offspring gene from two parent gene
    # using single point crossover return new offspring(s) gene
    def __single_point_gene_crossover(self,self_gene, other_gene):
        offspring_1 = [0] * self.n_chromosome
        # offspring_2 = [0] * self.n_chromosome
        crossover_point = random.randint(0, self.n_chromosome - 1)
        for i in range(self.n_chromosome):
            if (i <= crossover_point):
                offspring_1[i] = self_gene[i]
                # offspring_2[i] = other[i]
            else:
                offspring_1[i] = other_gene[i]
                # offspring_2[i] = other.chromosome[i]
        return offspring_1 #, offspring_2
    
    # crossover to creat one offspring from two parents using uniform crossover
    # create a random mask and based on mask[i] value will be
    # will consider to breed single offspring from parent
    def __uniform_crossover(self, other):
        offspring_1 = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring_1[i] = self.__uniform_gene_crossover(
                self_gene=self.chromosome[i], other_gene=other.chromosome[i])
        return Individual(self.variables_range, self.n_chromosome, self.n_gene, 
                          offspring_1, self.crossover_type, self.mutation_type)
    
    # crossover to creat one offspring from two parents using uniform crossover
    # create a random mask and based on mask[i] value will be
    # will consider to breed single offspring gene from parent gene
    def __uniform_gene_crossover(self,self_gene, other_gene):
        offspring_1 = [0] * self.n_chromosome
        # offspring_2 = [0] * self.n_chromosome
        mask = self.__generate_random_gene()
        for i in range(self.n_chromosome):
            if (mask[i] == 0):
                offspring_1[i] = self_gene[i]
                # offspring_2[i] = other.chromosome[i]
            else:
                offspring_1[i] = other_gene[i]
                # offspring_2[i] = self.chromosome[i]
        return offspring_1 #, offspring_2
    
    # mutate the individual
    def mutate(self):
        mutate_chromosome = None
        if (self.mutation_type == "bit_flip"):
            mutate_chromosome = self.__bit_flip_mutation()
        elif (self.mutation_type == "bit_swap"):
            # if (bits % 2 == 0):
            mutate_chromosome = self.__bit_swap_mutation()
            # else:
            #     print("invalid bit size for mutation")
            #     exit()
        else:
            print("invalid mutation type")
            exit()
        self.chromosome = mutate_chromosome  
    
    # bit flip mutation 
    def __bit_flip_mutation(self):
        offspring = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring[i] = self.__bit_flip_gene_mutation(self.chromosome[i])
        return offspring
    
    # bit flip mutation done by choosing random position of gene
    # and fliping the bit
    def __bit_flip_gene_mutation(self, gene, bits=2):
        offspring = gene.copy()
        flip_positions = [0] * bits
        for i in range(bits):
            flip_positions[i] = random.randint(0, self.n_chromosome - 1)
        for i in range(len(flip_positions)):
            pos = flip_positions[i]
            bit = offspring[pos]
            if bit == 0:
                offspring[pos] = 1
            else:
                offspring[pos] = 0
        return offspring
    
    # bit flip mutation 
    def __bit_swap_mutation(self):
        offspring = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring[i] = self.__bit_swap_gene_mutation(self.chromosome[i])
        return offspring  
    
    # bit swap mutation done by swaping the value at given bit position of
    # gene; bits must be even for swaping
    def __bit_swap_gene_mutation(self, gene, bits=2):
        offspring = gene.copy()
        swap_positions = [0] * bits
        for i in range(bits):
            swap_positions[i] = random.randint(0, self.n_chromosome - 1)
        i = 0
        while i < len(swap_positions):
            bit = offspring[swap_positions[i]]
            offspring[swap_positions[i]] = offspring[swap_positions[i+1]]
            offspring[swap_positions[i+1]] = bit
            i = i + 2
        return offspring
