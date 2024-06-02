import ast
import sys
import random
from evolution.random_object import RandomObject
from evolution.scanner import *
from evolution.testCase import *
from evolution.genome import *
from evolution.testSuite import *
from evolution.reproduction import *

from fitness.combine import fitness_score
import argparse
import pathlib


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
                if classObj.required_object_count[classObj2.name] == 0: continue
                # pairwise testing
                gen = Generation(self.target_code, self.finder, False, classObj1, classObj2)
                test_code += build_PairwiseTestCases(gen.evolve(threshold_score, max_generation))
        return test_code

class Generation():
    def __init__(self, target_code: str, finder, is_unit, classObj1, classObj2=None):
        print(classObj1.name)
        self.target_code = target_code
        self.current_population = [] # (testsuite, fitness)
        for _ in range(10):
            newTestSuite = TestSuite(is_unit)
            newTestSuite.random_testCaseList(finder.classList, classObj1, classObj2)
            test_code = newTestSuite.build_testcases()
            print(test_code)
            fitness = fitness_score(self.target_code, test_code)
            #print(self.target_code)
            print(fitness)
            self.current_population.append((newTestSuite, fitness))
        
    def next_generation(self):
        for i in range(5, 10):
            new_testCase = reproduce_testSuite(self.current_population[:5])
            test_code = new_testCase.build_testcases()
            fitness = fitness_score(self.target_code, test_code)
            #print(test_code)
            print(fitness)
            self.current_population[i] = (new_testCase, fitness)
        self.current_population.sort(key=lambda tup: tup[1], reverse=True)

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        for i in range(max_generation):
            print("top:", self.current_population[0][1])
            if self.current_population[0][1] > threshold_score:
                break
            self.next_generation()
        return self.current_population[0][0].testCaselist


def run_once(target_code: str) -> str:
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
    return test_code
