import ast
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    target = args.target
    sys.argv[1:] = args.remaining
    print("sys argv", sys.argv[1:])

    lines = (open(target, "r").readlines())
    root = ast.parse("".join(lines), target)

    print(ast.dump(root, include_attributes=False, indent=4))