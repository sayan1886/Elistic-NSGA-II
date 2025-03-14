# import sys
# from pathlib import Path

import matplotlib.pyplot as plt

# from nsga2.example.config import config
from core.evolution import Evolution
from core.problem import Problem


def f1(x):
    return x ** 2


def f2(x):
    return (x - 2) ** 2

def sch(schConfig):
    # executing_file_path = sys.argv[0]
    # example_name = Path(executing_file_path).stem
    # schConfig = config.get_config(example_name)
    # # schConfig = configs[0]
    # print(schConfig)
    
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
                    tournament_prob=schConfig.selection.tournament_probability,
                    crossover_prob=schConfig.crossover.crossover_probability,
                    mutation_prob=schConfig.mutation.mutation_probability)
    evolution = evo.evolve()
    func = [i.objectives for i in evolution]

    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    plt.title("MOO Benchmark Problem SCH")
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
