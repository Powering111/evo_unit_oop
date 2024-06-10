import ast
from evolution.random_object import RandomObject
from evolution.scanner import *
from evolution.testCase import *
from evolution.genome import *
from evolution.testSuite import *
from evolution.reproduction import *
from evolution.record_evolution import write_to_csv
from fitness import combine
from evolution.settings import *

def fitness_score(target_code: str, test_suite: TestSuite, class_name1: str, class_name2: str | None = None) -> float:
    test_code = test_suite.build_testcases()

    fitness_score = combine.fitness_score(target_code, test_code)
    return fitness_score

    fitness_score = combine.fitness_score_by_class(target_code, test_code)

    if class_name2 == None: 
        return fitness_score[class_name1]
    else:
        return (fitness_score[class_name1] + fitness_score[class_name2])/2


class Evolution():
    def __init__(self, target_code: str, target_name:str):
        self.finder = ClassFinder()
        self.finder.visit(ast.parse(target_code))
        self.target_code = target_code
        self.target_name = target_name
    def evolution(self, threshold_score: float, max_generation: int, csv_path=None):
        test_code = ""
        for classObj in self.finder.classList:
            # unittest
            gen = Generation(self.target_code, self.finder, True, classObj)
            test_code += build_UnitTestCases(gen.evolve(threshold_score, max_generation))
            write_to_csv(self.target_name, classObj.name, gen.record_fitness)
        for classObj1 in self.finder.classList:
            for classObj2 in self.finder.classList:
                if classObj1.required_object_count[classObj2.name] == 0: continue
                # pairwise testing
                gen = Generation(self.target_code, self.finder, False, classObj1, classObj2)
                test_code += build_PairwiseTestCases(gen.evolve(threshold_score, max_generation))
                write_to_csv(self.target_name, (classObj1.name+classObj2.name), gen.record_fitness)
        return test_code


# Generation is a collection of test suites.
# call *evolve* to run entire evolution.
class Generation():
    def __init__(self, target_code: str, finder: ClassFinder, is_unit: bool, classObj1: ClassScanner, classObj2: ClassScanner | None = None):
        self.target_code = target_code
        self.current_population = [] # (testsuite, fitness)
        self.classObj1 = classObj1
        self.classObj2 = classObj2
        self.class_name2 = None if classObj2==None else classObj2.name
        self.record_fitness = []
        if not QUIET: print("Generating for", self.classObj1.name, self.class_name2)
        for _ in range(POP_PER_GEN):
            newTestSuite = TestSuite(is_unit)
            newTestSuite.random_testCaseList(finder.classList, classObj1, classObj2)
            #print(test_code)
            fitness = fitness_score(self.target_code, newTestSuite, self.classObj1.name, self.class_name2)
            #print(self.target_code)
            if VERBOSE: print(fitness)
            self.current_population.append((newTestSuite, fitness))

    def next_generation(self):
        for i in range(KEEP_CLEAN, POP_PER_GEN):
            if i < KEEP_MUT:
                mutate(self.current_population[i][0], self.classObj1, self.classObj2)
                new_testSuite = self.current_population[i][0]
            else: 
                new_testSuite = reproduce_testSuite(self.current_population[:KEEP_MUT])
                mutate(new_testSuite, self.classObj1, self.classObj2)
            fitness = fitness_score(self.target_code, new_testSuite, self.classObj1.name, self.class_name2)
            #print(test_code)
            if VERBOSE: print(fitness)
            self.current_population[i] = (new_testSuite, fitness)

    
    def evolve(self, threshold_score: float, max_generation: int) -> list[UnitTestCase|PairwiseTestCase]:
        for i in range(max_generation):
            self.current_population.sort(key=lambda tup: tup[1], reverse=True)
            self.record_fitness.append([tup[1] for tup in self.current_population])
            if VERBOSE: print("top:", self.current_population[0][1])
            if self.current_population[0][1] >= threshold_score:
                break
            self.next_generation()
        if not QUIET: print(self.current_population[0][1])
        return self.current_population[0][0].testCaselist
