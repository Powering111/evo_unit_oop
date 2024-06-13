# this code runs crossover between two test suites.
# They are saved in record directory.
# record/suite0.py and record/suite1.py is combined(crossover)
# to record/suite0_1.py


from evolution.reproduction import *
from evolution.genome import *
from evolution.evolve import *
import pathlib
import ast
import os
import random

target_code = pathlib.Path("testcases/dummy.py").read_text()

finder = ClassFinder()
finder.visit(ast.parse(target_code))

print([scanner.name for scanner in finder.classList])

generation = Generation(target_code, finder, True, finder.classList[0])

(ts0,fit0) = generation.current_population[0]
(ts1,fit1) = generation.current_population[1]



ts0_1 = TestSuite(True)
for _ in range(5):
    mom_index = random.randint(0, 24)
    dad_index = random.randint(0, 24)
    mom = ts0.testCaselist[mom_index%5]
    dad = ts1.testCaselist[dad_index%5]
    ts0_1.testCaselist.append(mix_testCase(True, mom,dad))

if not os.path.isdir(f"record"):
    os.makedirs(f"record")

pathlib.Path("record/suite0.py").write_text(ts0.build_testcases())
pathlib.Path("record/suite1.py").write_text(ts1.build_testcases())

pathlib.Path("record/suite0_1.py").write_text(ts0_1.build_testcases())
