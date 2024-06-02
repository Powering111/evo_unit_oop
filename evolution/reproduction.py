import random
import sys
from evolution.testSuite import *

def crossover(lst1, lst2):
    cross_point1 = random.randrange(0, len(lst1)+1)
    cross_point2 = random.randrange(0, len(lst2)+1)
    return lst1[:cross_point1]+lst2[cross_point2:]

def mix_genome(genome1, genome2): 
    new_genome = genome1 if bool(random.getrandbits(1)) else genome2
    new_genome.methodCall_lst = crossover(genome1.methodCall_lst, genome2.methodCall_lst)
    return new_genome

def mix_testCase(is_unit, testCase1, testCase2):
    # mix surrounding_objs
    new_surr_objs = []
    for obj1, obj2 in zip(testCase1.surrounding_objs, testCase2.surrounding_objs):
        if random.getrandbits(1):
            new_surr_objs.append(obj1)
        else: new_surr_objs.append(obj2)
    if is_unit:
        new_main_obj = mix_genome(testCase1.main_obj, testCase2.main_obj)
        return UnitTestCase(new_main_obj, new_surr_objs)
    else:
        new_main_obj1 =  mix_genome(testCase1.main_obj1, testCase2.main_obj1)
        new_main_obj2 =  mix_genome(testCase1.main_obj2, testCase2.main_obj2)
        return PairwiseTestCase(new_main_obj1, new_main_obj2, new_surr_objs)

def reproduce_testSuite(prevgen_testSuites):
    is_unit = prevgen_testSuites[0][0].is_unit
    new_testSuite = TestSuite(is_unit)
    for _ in range(5):
        mom_index = random.randint(0, 24)
        dad_index = random.randint(0, 24)
        mom = prevgen_testSuites[mom_index//5][0].testCaselist[mom_index%5]
        dad = prevgen_testSuites[dad_index//5][0].testCaselist[dad_index%5]
        new_testSuite.testCaselist.append(mix_testCase(is_unit, mom, dad))
    #mutate(new_testSuite)
    return new_testSuite


# MUTATE 20% of the population
MUTATION_PROB = 0.2
# EACH MUTATION WILL YIELD DIFFERENCE OF 10%
MUTATION_SEVERITY = 0.1
def mutate_methodCall(methodCall):
    if methodCall == None: return
    for i, arg in enumerate(methodCall.args):
        if isinstance(arg, int):
            print("hihi", arg)
            print(type(methodCall.args))
def mutate_genome(genome):
    pass
def mutate(testSuite):
    if not testSuite.is_unit: return
    for testCase in testSuite.testCaselist:
        for assertion, _ in testCase.main_obj.methodCall_lst: 
            mutate_methodCall(assertion.MethodCall)
            