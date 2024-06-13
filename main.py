import sys
import argparse
import pathlib
from evolution.evolve import Evolution
from fitness import combine
from fitness.helper import get_full_testsuite_code
from evolution.settings import GENERATION

# TEST_HEADER = lambda module_name: f"""
# import sys
# import os
# curr_dir = os.getcwd()
# sys.path.insert(1, curr_dir)
#
# import {module_name} as target
#
# """
TEST_HEADER = lambda _: f"""
import target

"""

def evolution (target) : 
    target_code = target.read_text()
    evo_test_code =  Evolution(target_code, str(target.stem)).evolution(0.9, GENERATION)
    
    full_test_code = get_full_testsuite_code("import target\n" + evo_test_code)
    full_test_code = '\n'.join(line for line in full_test_code.split('\n') if line != "import target")

    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")
    module_name = str(target).replace(pathlib.os.sep, '.')[:-3]
    to_write = TEST_HEADER(module_name) + full_test_code

    path_to_write.write_text(to_write)
    print("Written to ", path_to_write)

    combine.fitness_score(target_code, "import target\n"+full_test_code, verbose=True)

def fitness (target, suite) :
    target_code = target.read_text()
    suite_code = suite.read_text()

    combine.fitness_score(target_code, suite_code, verbose=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('command', nargs=1)
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument('-s', '--suite')
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    ########### check validity of the target ################################
    target = pathlib.Path(args.target)
    if target.suffix != '.py':
        parser.error('Argument error: target has to be .py file')
    if not (target.exists() and target.is_file()):
        parser.error('Argument error: target has to be an existing file')

    suite = None
    if args.suite: 
        suite = pathlib.Path(args.suite)
        if suite.suffix != '.py':
            parser.error('Argument error: suite has to be .py file')
        if not (suite.exists() and suite.is_file()):
            parser.error('Argument error: suite has to be an existing file')
    #########################################################################   

    sys.argv[1:] = args.remaining
    command = args.command[0]
    
    if command == "evolution" : 
        evolution(target)
    if command == "fitness" : 
        fitness(target, suite)
