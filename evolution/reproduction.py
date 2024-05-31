import random
from . import evolution
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .evolution import Genome as Genome

def reproduce(lst1, lst2):
    cross_point1 = random.randrange(1, len(lst1[0])+1)
    cross_point2 = random.randrange(1, len(lst2[0])+1)
    return (lst1[0][:cross_point1]+lst2[0][cross_point2:], 0)

def roulette(pop):
    fitness = np.array([gene[1] for gene in pop])
    qs = np.cumsum(fitness)
    thres = random.uniform(0, qs[-1])
    thres = min(thres, random.uniform(0, qs[-1]))   # EVEN MORE BIASED TOWARD BETTER ORGANISM
    return np.argmax(qs > thres)
    
def generate_newgen(prevgen):
    newgen = []
    for _ in range(len(prevgen)):
        mom = prevgen[roulette(prevgen)]
        dad = prevgen[roulette(prevgen)]
        newgen.append(reproduce(mom, dad))
    return newgen


# MUTATE 20% of the population
MUTATION_PROB = 0.2
# EACH MUTATION WILL YIELD DIFFERENCE OF (10%)^2
MUTATION_SEVERITY = 0.1


def mutate(population):
    for i, _ in enumerate(population):
        if random.random() < MUTATION_PROB:
            mutate_gene(population[i])
    return population

def mutate_gene(genomeList: list["Genome"]):
        for i, _ in enumerate(genomeList):
                if random.random() < MUTATION_SEVERITY:
                    pass
                return genomeList

