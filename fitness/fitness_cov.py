


# Assuming that the format of the target class would be a file containing import statements and classes.
# And the test suite would be a file containing just multiple functions and nothing else.

# This program only works on unix-like system.

import subprocess as sp
import json
import os
import ast

def write_target (target_code: str, test_suite: str) : 
    with open ('target.py', 'w') as f: 
        f.write(target_code) 
    with open('test.py', 'w') as f:
        f.write(test_suite)


# Given the target python class in string `target_code` and given the test-suite in string `test_suite`
# Run the the test_suite and return the corresponding coverage object
def get_coverage (target_code: str, test_suite_code: str) -> dict:
    root = ast.parse(test_suite_code)
    print(ast.dump(root,indent=2))

    # slightly change code to run test functions.
    test_functions = [] # name of the test functions
    for elem in root.body:
        if isinstance(elem, ast.FunctionDef):
            test_functions.append(elem.name)
            test_suite_code += f'\n{elem.name}()'

    # run coverage.py
    os.chdir('tmp/')
    write_target(target_code, test_suite_code)
    
    sp.run("python3.11 -m coverage run --branch test.py", shell=True, check=True)
    sp.run("python3.11 -m coverage json --pretty-print -o cov.json", shell=True, check=True, capture_output=True)

    # get result
    result_file = open('cov.json', 'r')
    result_obj = json.load(result_file)
    result_file.close()

    assert('files' in result_obj.keys())
    assert('target.py' in result_obj['files'])

    return result_obj['files']['target.py']


if __name__ == "__main__" :
    with open("testcases/dummy.py") as f:
        target_code = f.read()
    with open("testcases/dummy_test.py") as f:
        test_suite = f.read()

    c = get_coverage(target_code, test_suite)
    print(c)

