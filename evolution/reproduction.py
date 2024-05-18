import random 
import sys

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

# MUTATE HOW 20% of the population
MUTATION_PROB = 0.2
# EACH MUTATION WILL YIELD DIFFERENCE OF 10%
MUTATION_SEVERITY = 0.1

def mutate(genomeList):
    for i, _ in enumerate(genomeList) :
        if random.random() < MUTATION_PROB :
            mutate_methodCall(genomeList[i].methodCall_lst)

def mutate_methodCall (methodCalls) : 
    for i, mc in enumerate(methodCalls): 
        if random.random() < MUTATION_SEVERITY :
            priority = random.randint(-sys.maxsize - 1, sys.maxsize)
            methodCalls[i] = (mc[0], priority)
