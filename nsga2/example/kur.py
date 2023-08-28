from nsga2.core.problem import Problem
from nsga2.core.evolution import Evolution
import matplotlib.pyplot as plt
import math


def f1(x):
    s = 0
    for i in range(len(x) - 1):
        s += -10 * math.exp(-0.2 * math.sqrt(x[i] ** 2 + x[i + 1] ** 2))
    return s


def f2(x):
    s = 0
    for i in range(len(x)):
        s += abs(x[i]) ** 0.8 + 5 * math.sin(x[i] ** 3)
    return s


problem = Problem(num_of_variables=3 ,objectives=[f1, f2], variables_range=[(-5, 5)], 
                  same_range=False, expand=False, n_chromosome=16)
evo = Evolution(problem, num_of_individuals=150,num_of_generations=1000)
func = [i.objectives for i in evo.evolve()]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.title("MOO Benchmark Problem KUR")
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
