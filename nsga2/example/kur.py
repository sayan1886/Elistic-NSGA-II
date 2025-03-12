# import sys
# from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from nsga2.core.problem import Problem
from nsga2.core.evolution import Evolution


def f1(x):
    s = 0
    for i in range(len(x) - 1):
        s += -10 * np.exp(-0.2 * (np.sqrt(x[i] ** 2 + x[i + 1] ** 2)))
    return s


def f2(x):
    s = 0
    for i in range(len(x)):
        s += (np.abs(x[i]) ** 0.8) + (5 * np.sin(x[i] ** 3))
    return s

def kur(kurConfig):
    # executing_file_path = sys.argv[0]
    # example_name = Path(executing_file_path).stem
    # kurConfig = config.get_config(example_name)
    # # kurConfig = configs
    # print(kurConfig)
    
    problem = Problem(objectives=[f1, f2], 
                      num_of_variables=kurConfig.num_of_gene, 
                      variables_range=[(kurConfig.range.min, kurConfig.range.max)],
                      expand=kurConfig.objective.expand, 
                      same_range=kurConfig.range.variable_range, 
                      n_chromosome=kurConfig.num_of_chromosomes)
    
    evo = Evolution(problem=problem, 
                    num_of_generations=kurConfig.num_of_generations, 
                    num_of_individuals=kurConfig.num_of_individuals, 
                    num_of_tour_particips=kurConfig.selection.participants,
                    tournament_prob=kurConfig.selection.tournament_probability,
                    crossover_prob=kurConfig.crossover.crossover_probability,
                    mutation_prob=kurConfig.mutation.mutation_probability)
    
    func = [i.objectives for i in evo.evolve()]

    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    plt.title("MOO Benchmark Problem KUR")
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
