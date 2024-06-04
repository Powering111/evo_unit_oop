import sys
import argparse
import pathlib
from collections import defaultdict
from evolution.evolve import Evolution
from fitness import combine

TEST_SUITE_HEADER = lambda m: f"""
# import sys
# import os
# curr_dir = os.getcwd()
# sys.path.insert(1, curr_dir)

# import {m} as target
"""

def evolution (target) : 
    target_code = target.read_text()
    final_test_code =  Evolution(target_code, str(target.stem)).evolution(0.9, 10)

    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")
    module_name = str(target).replace(pathlib.os.sep, '.')[:-3]

    to_write = TEST_SUITE_HEADER(module_name) + final_test_code
    path_to_write.write_text(to_write)

    ######################################################
    combine.fitness_score(target_code, "import target\n"+final_test_code, verbose=True)

def fitness (target, suite): 
    target_code = target.read_text()
    suite_code = "import target\n" + suite.read_text()
    combine.fitness_score(target_code, suite_code, verbose=True)
    combine.fitness_score_by_class(target_code, suite_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument("command", nargs=1)
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument('-s', '--suite', )
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    ############ check validity of the files ##############################
    target = pathlib.Path(args.target)
    if target.suffix != '.py':
        parser.error('Argument error: target has to be .py file')
    if not (target.exists() and target.is_file()):
        parser.error('Argument error: target has to be an existing file')

    suite = None
    if args.suite is not None: 
        suite = pathlib.Path(args.suite)
        if suite.suffix != '.py':
            parser.error('Argument error: target has to be .py file')
        if not (suite.exists() and suite.is_file()):
            parser.error('Argument error: target has to be an existing file')
    ########################################################################

    sys.argv[1:] = args.remaining
    cmd = args.command[0]

    if cmd == "evolution": 
        evolution(target)
    if cmd == "fitness": 
        if suite is None: 
            parser.error('Test Suite needed for fitness call')
        fitness(target, suite)
    
