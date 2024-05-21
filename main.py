import sys
import argparse
import pathlib
from evolution import evolution 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    target = pathlib.Path(args.target)
    # check validity of the target
    if target.suffix != '.py':
        parser.error('Argument error: target has to be .py file')
    if not (target.exists() and target.is_file()):
        parser.error('Argument error: target has to be an existing file')

    sys.argv[1:] = args.remaining

    target_code = target.read_text()
    final_test_code = evolution.run_evolution(target_code)

    path_to_write = (target.parent / "testsuites" / f"test_{target.stem}.py")
    print(path_to_write)
    print(final_test_code)
    with open(path_to_write, 'w') as f:
        f.write(final_test_code)

