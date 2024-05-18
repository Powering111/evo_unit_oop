from evolution import Genome
from evolution import MethodCall
import random

def mix_init(genome1, genome2):
    return genome1 if bool(random.getrandbits(1)) else genome2
    
def crossover(lst1, lst2):
    cross_point1 = random.randrange(0, len(lst1)+1)
    cross_point2 = random.randrange(0, len(lst2)+1)
    return lst1[:cross_point1]+lst2[cross_point2:]

def reproduce(genome1, genome2):
    kid_genome = mix_init(genome1, genome2)
    kid_genome.set_methodCall_lst(crossover(genome1.methodCall_lst, genome2.methodCall_lst))
    return kid_genome

def generate_newgen(prevgen):
    newgen = []
    for i in range(len(prevgen)):
        mom =  prevgen[random.randrange(0, len(prevgen))]
        dad =  prevgen[random.randrange(0, len(prevgen))]
        newgen.append(reproduce(mom, dad))
    return newgen

lst1 = [1,2,3,4,5]
lst2=[11,12,13,14,15]
for i in range(10):
    print(crossover(lst1, lst2))