import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from nsga2.example.config import config
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

if __name__ == "__main__":
    executing_file_path = sys.argv[0]
    example_name = Path(executing_file_path).stem
    configs = config.get_config(example_name)
    schConfig = configs[0]
    print(schConfig)
    
    problem = Problem(objectives=[f1, f2], 
                      num_of_variables=schConfig.num_of_gene, 
                      variables_range=[(schConfig.range.min, schConfig.range.max)],
                      expand=schConfig.objective.expand, 
                      same_range=schConfig.range.variable_range, 
                      n_chromosome=schConfig.num_of_chromosomes)
    
    evo = Evolution(problem=problem, 
                    num_of_generations=schConfig.num_of_generations, 
                    num_of_individuals=schConfig.num_of_individuals, 
                    num_of_tour_particips=schConfig.selection.participants,
                    tournament_prob=schConfig.selection.tournament_probabilty,
                    crossover_prob=schConfig.crossover.crossover_probabilty,
                    mutation_prob=schConfig.mutation.mutation_probabilty)
    
    # problem = Problem(num_of_variables=3 ,objectives=[f1, f2], variables_range=[(-5, 5)], 
    #                 same_range=False, expand=False, n_chromosome=16)
    # evo = Evolution(problem, num_of_individuals=150,num_of_generations=1000)
    
    func = [i.objectives for i in evo.evolve()]

    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    plt.title("MOO Benchmark Problem KUR")
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
