import random
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .evolution import Genome as Genome

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .evolution import Genome as Genome

def reproduce(lst1, lst2):
    cross_point1 = random.randrange(1, len(lst1[0])+1)
    cross_point2 = random.randrange(1, len(lst2[0])+1)
    return (lst1[0][:cross_point1]+lst2[0][cross_point2:], 0)


def generate_newgen(prevgen):
    newgen = []
    for _ in range(2*len(prevgen)):
        mom = prevgen[random.randrange(0, len(prevgen))]
        dad = prevgen[random.randrange(0, len(prevgen))]
        newgen.append(reproduce(mom, dad))
    return newgen


# MUTATE 20% of the population
MUTATION_PROB = 0.2
# EACH MUTATION WILL YIELD DIFFERENCE OF 10%
MUTATION_SEVERITY = 0.1


def mutate(population):
    for i, _ in enumerate(population):
        if random.random() < MUTATION_PROB:
            mutate_gene(population[i])
    return population

def mutate_gene(gene): # TODO
    return gene
