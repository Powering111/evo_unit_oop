import random
import sys
from evolution.testSuite import *

def crossover(lst1, lst2):
    cross_point1 = random.randrange(0, len(lst1)+1)
    cross_point2 = random.randrange(0, len(lst2)+1)
    return lst1[:cross_point1]+lst2[cross_point2:]

def mix_genome(genome1, genome2): 
    new_genome = genome1 if bool(random.getrandbits(1)) else genome2
    #new_genome.methodCall_lst = crossover(genome1.methodCall_lst, genome2.methodCall_lst)
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
    return new_testSuite


# MUTATE 30% of the population
MUTATION_PROB = 0.3

def mutate_int(i):
    #print("mutate int")
    if random.random() > MUTATION_PROB: return i
    index = random.random()
    if index < 0.2: return i+1
    elif index < 0.4: return i-1
    elif index < 0.6: return -i
    else: random.randint(-sys.maxsize - 1, sys.maxsize)

def mutate_str(str):
    #print("mutate str")
    if random.random() > MUTATION_PROB: return str
    index=random.random()
    str = str.replace("\"","")
    if index < 0.2: return_str = str[1:]
    elif index < 0.4: return_str = str[:-1]
    elif index < 0.6: return_str = crossover(str, str)
    else: return RandomObject().rand_str()
    return f'"{return_str}"'

def mutate_float(f):
    #print("mutate float")
    if random.random() > MUTATION_PROB: return f
    index = random.random()
    if index < 0.2: return f*2
    elif index < 0.4: return f/2
    elif index < 0.6: return -f
    else: return random.uniform(-sys.maxsize - 1, sys.maxsize)

def mutate_args(target):
    if target == None: return
    for i, arg in enumerate(target.args):
        if isinstance(arg, int):
            target.args[i] = mutate_int(arg)
        elif isinstance(arg, str):
            target.args[i] = mutate_str(arg)
        elif isinstance(arg, float):
            target.args[i] = mutate_float(arg)

def mutate_MClist(main_obj, classObj1, classObj2=None):
    if random.random() > MUTATION_PROB: return
    index = random.random()
    if index < 0.3: add_random_to_MClist(main_obj, classObj1, classObj2)
    elif index < 0.6:
        cut_point = random.randint(0, len(main_obj.methodCall_lst)-1)
        main_obj.methodCall_lst = main_obj.methodCall_lst[cut_point:]
    else:
        for i, (assertion, priority) in enumerate(main_obj.methodCall_lst):
            new_priority = random.randint(-sys.maxsize - 1, sys.maxsize)
            main_obj.methodCall_lst[i] = (assertion, new_priority)
    #print(main_obj.methodCall_lst)


def add_random_to_MClist(main_obj, classObj1, classObj2):
    if classObj2==None:
        classObj1.required_object_count[classObj1.name]+=1
        rand_device = RandomObject(classObj1.required_object_count)
        classObj1.required_object_count[classObj1.name]-=1
    else:
        required_sub_obj = defaultdict(int)
        # merge required_object_count for class1 and class2
        for d in (classObj1.required_object_count, classObj2.required_object_count):
            for k, v in d.items():
                required_sub_obj[k] = max(required_sub_obj[k], v)
        required_sub_obj[classObj1.name]+=1
        required_sub_obj[classObj2.name]+=1
        rand_device = RandomObject(required_sub_obj)
        required_sub_obj[classObj1.name]-=1
        required_sub_obj[classObj2.name]-=1
    add_random_methodcall_sequence(classObj1, main_obj, rand_device)

def mutate(testSuite, classObj1, classObj2):
    if testSuite.is_unit: 
        for testCase in testSuite.testCaselist:
            if random.random() > MUTATION_PROB: continue
            # mutate main_obj
            mutate_args(testCase.main_obj)
            mutate_MClist(testCase.main_obj, classObj1)
            # mutate arguments of methodCall_lst of the main_obj
            for assertion, _ in testCase.main_obj.methodCall_lst: 
                mutate_args(assertion.MethodCall)
            # mutate surrounding_objs
            for obj in testCase.surrounding_objs:
                if random.random() > MUTATION_PROB: mutate_args(obj)
    else: 
        for testCase in testSuite.testCaselist:
            if random.random() > MUTATION_PROB: continue
            # mutate main_obj
            mutate_args(testCase.main_obj1)
            mutate_args(testCase.main_obj2)
            mutate_MClist(testCase.main_obj1, classObj1, classObj2)
            mutate_MClist(testCase.main_obj2, classObj2, classObj1)
            # mutate arguments of methodCall_lst of the main_obj
            for assertion, _ in testCase.main_obj1.methodCall_lst: 
                mutate_args(assertion.MethodCall)
            for assertion, _ in testCase.main_obj2.methodCall_lst: 
                mutate_args(assertion.MethodCall)
            # mutate surrounding_objs
            for obj in testCase.surrounding_objs:
                if random.random() > MUTATION_PROB: mutate_args(obj)