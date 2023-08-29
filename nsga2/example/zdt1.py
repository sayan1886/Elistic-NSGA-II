import sys
from pathlib import Path

import matplotlib.pyplot as plt

from nsga2.example.config import config
from nsga2.core.evolution import Evolution
from nsga2.core.problem import Problem


def f1(x):
    return x[0]

def f2(x):
    g_x = g(x)
    f2_x = g_x * (1 - (x[0] / g_x) ** 0.5)
    return f2_x

def g(x):
    g_x = 1 + 9 * (sum(x[1:len(x)]) / len(x) - 1)
    return g_x

def sum(x):
    sum = 0
    for i in range(len(x)):
        sum += x[i]
    return sum

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
    evol = evo.evolve()
    func = [i.objectives for i in evol]

    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    plt.title("MOO Benchmark Problem ZDT1")
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
