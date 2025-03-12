# import sys
# from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# from nsga2.example.config import config
from nsga2.core.evolution import Evolution
from nsga2.core.problem import Problem

# f1(x) = x
def f1(x):
    return x[0]

# f2(x) = g(x) * [1 - (x1/g(x) ^ 0.5)] , x1 = 0, xi = 0, i = 2.....30
def f2(x):
    g_x = g(x)
    f2_x = g_x * (1 - np.sqrt(f1(x) / g_x))
    return f2_x

# g(x) = 1 + 9 * sum(xi) / (n - 1), i = 2, ...., n, n = 30
def g(x):
    g_x = 1 + 9 * np.sum(x) / len(x) - 1
    return g_x

def zdt1(zdtOneConfig):
    # executing_file_path = sys.argv[0]
    # example_name = Path(executing_file_path).stem
    # zdtOneConfig = config.get_config(example_name)
    # # zdtOneConfig = configs[0]
    # print(zdtOneConfig)
    
    problem = Problem(objectives=[f1, f2], 
                      num_of_variables=zdtOneConfig.num_of_gene, 
                      variables_range=[(zdtOneConfig.range.min, zdtOneConfig.range.max)],
                      expand=zdtOneConfig.objective.expand, 
                      same_range=zdtOneConfig.range.variable_range, 
                      n_chromosome=zdtOneConfig.num_of_chromosomes)
    
    evo = Evolution(problem=problem, 
                    num_of_generations=zdtOneConfig.num_of_generations, 
                    num_of_individuals=zdtOneConfig.num_of_individuals, 
                    num_of_tour_particips=zdtOneConfig.selection.participants,
                    tournament_prob=zdtOneConfig.selection.tournament_probability,
                    crossover_prob=zdtOneConfig.crossover.crossover_probability,
                    mutation_prob=zdtOneConfig.mutation.mutation_probability)
    evolution = evo.evolve()
    func = [i.objectives for i in evolution]

    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    plt.title("MOO Benchmark Problem ZDT1")
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
