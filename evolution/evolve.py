import ast
import sys
import random
from evolution.random_object import RandomObject
from evolution.scanner import ClassScanner
from evolution.scanner import ClassFinder
from evolution import reproduction
from fitness.combine import fitness_score

POP_SIZE = 5 

# method call code string
class MethodCall():
    def __init__(self, class_name, method_name, *args, **kwargs):
        self.method_name = method_name
        self.class_name = class_name
        self.args = args
        self.kwargs = kwargs

    def call_str(self):
        arg_list = []
        for arg in self.args:
            arg_list.append(str(arg))
        for key, val in self.kwargs.items():
            arg_list.append(f"{key}={val}")
        return f".{self.method_name}({', '.join(arg_list)})"

class Assertion():
    def __init__(self, class_name, methodcall, attr_name):
        self.class_name = class_name
        self.MethodCall = methodcall
        self.attr = attr_name

# Test case for a class
class Genome(): #1:1 with an object
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_args = args
        self.init_kwargs = kwargs
        self.methodCall_lst = [] #(methodCall/Assertion, int)
    def set_methodCall_lst(self, methodCall_lst):
        self.methodCall_lst = methodCall_lst

    def add_methodcall(self, methodcall, priority: int):
        self.methodCall_lst.append((methodcall, priority))

    def __str__(self):
        meta = f"genome for {self.class_name}: a={self.init_args} kw={self.init_kwargs}"
        gene = "\n\t".join(str(mc) for mc in self.methodCall_lst)
        return meta + '\n\t' + gene

# Generate MethodCall object with random values
def RandomMethodCall(Class:ClassScanner, method_name:str, rand_device:RandomObject):
    method_args = Class.method_args[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(f"obj_{Class.name}{i}")
        else:
            args.append(getattr(rand_device, f"rand_{arg_type}")())
    return MethodCall(Class.name, method_name, *args)

def sort_pop (pop) :
    return sorted(pop, key=lambda x: -x[1])

class Generation():
    def __init__(self, target_code: str):
        self.finder = ClassFinder()
        self.finder.visit(ast.parse(target_code))
        self.finder.report() # debug
        self.target_code = target_code

    def get_fitness(self, genomeList: list[Genome]) -> float:
        test_code = build_test(genomeList)
        score = fitness_score(self.target_code, test_code)
        return score

    def make_pop (self, pop) :
        fit = [self.get_fitness(p) for p in pop]
        return list(zip(pop, fit))

    def recalculate_fitness(self, pop): 
        pop = [p[0] for p in pop]
        fit = [self.get_fitness(p) for p in pop]
        return list(zip(pop, fit))

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        pop = generatePopulation(self.finder.classList)
        pop = self.make_pop(pop)
        # pop = sort_pop(pop)
        for _ in range(max_generation):
            pop = reproduction.generate_newgen(pop)
            pop = reproduction.mutate(pop)
            pop = self.recalculate_fitness(pop)
            pop = sort_pop(pop)
            pop = pop[:POP_SIZE]

            print("leading fitness: ", pop[0][1])

            if pop[0][1] > threshold_score : break
            
        return pop[0][0]

def generatePopulation (classList):
    return [generateGenomeList(classList) for _ in range(POP_SIZE)]



def run_evolution(target_code: str, threshold_score: float = 0.8, max_generation: int = 10) -> str:

    genomeList = Generation(target_code).evolve(threshold_score, max_generation)
    test_code = build_test(genomeList)

    return test_code
