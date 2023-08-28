from nsga2.core.evolution import Evolution
from nsga2.core.problem import Problem
import matplotlib.pyplot as plt


def f1(x):
    return x ** 2


def f2(x):
    return (x - 2) ** 2


problem = Problem(num_of_variables=1, objectives=[f1, f2], variables_range=[(0, 2)],
                  expand=True, same_range=False, n_chromosome=16)
evo = Evolution(problem, num_of_generations=100, num_of_individuals=100, 
                tournament_prob=1.0)
evol = evo.evolve()
func = [i.objectives for i in evol]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.title("MOO Benchmark Problem SCH")
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
