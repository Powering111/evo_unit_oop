import ast
import sys
import random
from evolution.random_object import RandomObject
from evolution.scanner import *
from evolution.testCase import *
from evolution.genome import *
from evolution.testSuite import *
from evolution.reproduction import *

from fitness.combine import fitness_score_by_class
import argparse
import pathlib

def fitness_score(target_code, test_Suite, class_name1, class_name2):
    test_code = test_Suite.build_testcases()
    fitness_score = fitness_score_by_class(target_code, test_code)
    #print(fitness_score)
    if class_name2 == None: 
        return fitness_score[class_name1]
    else:
        return (fitness_score[class_name1] + fitness_score[class_name2])/2

class Evolution():
    def __init__(self, target_code: str):
        self.finder = ClassFinder()
        self.finder.visit(ast.parse(target_code))
        self.target_code = target_code
    def evolution(self, threshold_score: float, max_generation: int):
        test_code = ""
        for classObj in self.finder.classList:
            # unittest
            gen = Generation(self.target_code, self.finder, True, classObj)
            test_code += build_UnitTestCases(gen.evolve(threshold_score, max_generation))
        for classObj1 in self.finder.classList:
            for classObj2 in self.finder.classList:
                if classObj1.required_object_count[classObj2.name] == 0: continue
                # pairwise testing
                gen = Generation(self.target_code, self.finder, False, classObj1, classObj2)
                test_code += build_PairwiseTestCases(gen.evolve(threshold_score, max_generation))
        return test_code

class Generation():
    def __init__(self, target_code: str, finder, is_unit, classObj1, classObj2=None):
        self.target_code = target_code
        self.current_population = [] # (testsuite, fitness)
        self.class_name1 = classObj1.name
        self.class_name2 = None if classObj2==None else classObj2.name
        print(self.class_name1, self.class_name2)
        for _ in range(10):
            newTestSuite = TestSuite(is_unit)
            newTestSuite.random_testCaseList(finder.classList, classObj1, classObj2)
            #print(test_code)
            fitness = fitness_score(self.target_code, newTestSuite, self.class_name1, self.class_name2)
            #print(self.target_code)
            print(fitness)
            self.current_population.append((newTestSuite, fitness))
        
    def next_generation(self):
        for i in range(5, 10):
            new_testSuite = reproduce_testSuite(self.current_population[:5])
            fitness = fitness_score(self.target_code, new_testSuite, self.class_name1, self.class_name2)
            #print(test_code)
            print(fitness)
            self.current_population[i] = (new_testSuite, fitness)

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        for i in range(max_generation):
            self.current_population.sort(key=lambda tup: tup[1], reverse=True)
            print("top:", self.current_population[0][1])
            if self.current_population[0][1] >= threshold_score:
                break
            self.next_generation()
        return self.current_population[0][0].testCaselist


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

    
    test_code = "import hello as target\n"
    test_code += Evolution(target_code).evolution(0.9, 10)
    
    with open(path_to_write, 'w') as f:
        f.write(test_code)

    #score = fitness_score(target_code, test_code)
    #print(score)