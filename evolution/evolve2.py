import ast
import sys
import random
from evolution.random_object import RandomObject
from evolution.scanner import *
from evolution.testCase import *
from evolution.genome import *
from evolution import reproduction

from fitness.combine import fitness_score
import argparse
import pathlib

POP_SIZE = 5 

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
        #score = fitness_score(self.target_code, test_code)
        return 0

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


def run_evolution(target_code: str, threshold_score: float = 0.8, max_generation: int = 10) -> str:

    genomeList = Generation(target_code).evolve(threshold_score, max_generation)
    test_code = build_test(genomeList)

    return test_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('-t', '--target', required=True)
    #parser.add_argument('-c', '--targetClass', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    target = pathlib.Path(args.target)
    #target_class = args.targetClass
    #print(target_class, type(target_class))
    # check validity of the target
    if target.suffix != '.py':
        parser.error('Argument error: target has to be .py file')
    if not (target.exists() and target.is_file()):
        parser.error('Argument error: target has to be an existing file')

    sys.argv[1:] = args.remaining

    target_code = target.read_text()
    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")

    finder = ClassFinder()
    finder.visit(ast.parse(target_code))
    test_code = "import target\n"
    for classObj in finder.classList:
        # unittest
        tclist = generate_UnitTestCase_List(finder.classList, classObj)
        test_code += build_UnitTestCases(tclist)
        for classObj2 in finder.classList:
            if classObj.required_object_count[classObj2.name] == 0: continue
            # pairwise testing
            tclist = generate_PairwiseTestCase_List(finder.classList, classObj, classObj2)
            test_code += build_PairwiseTestCases(tclist)
    
    with open(path_to_write, 'w') as f:
        f.write(test_code)

    #score = fitness_score(target_code, test_code)
    #print(score)