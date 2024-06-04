import sys
import argparse
import pathlib
from evolution.evolve import Evolution
from fitness import combine

TEST_HEADER = lambda module_name: f"""
import sys
import os
curr_dir = os.getcwd()
sys.path.insert(1, curr_dir)

import {module_name} as target

"""

def evolution (target) : 
    target_code = target.read_text()
    final_test_code =  Evolution(target_code, str(target.stem)).evolution(0.9, 10)

    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")
    module_name = str(target).replace(pathlib.os.sep, '.')[:-3]
    to_write = TEST_HEADER(module_name) + final_test_code

    path_to_write.write_text(to_write)

    combine.fitness_score(target_code, "import target\n"+final_test_code, verbose=True)

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
        pass
