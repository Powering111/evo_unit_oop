import sys
import argparse
import pathlib
from collections import defaultdict
from evolution import evolve
from fitness import combine

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
    final_test_code = evolve.run_once(target_code)

    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")
    path_to_write.write_text(final_test_code)

    ######################################################

    combine.fitness_score(target_code, final_test_code, verbose=True)
