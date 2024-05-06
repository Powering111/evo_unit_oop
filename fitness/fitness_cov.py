# Assuming that the format of the target class would be a file containing import statements and classes.
# And the test suite would be a file containing just multiple functions and nothing else.

import subprocess as sp
import json
import os
import make_target

# Given the target python class in string `target_code` and given the test-suite in string `test_suite`
# Run the the test_suite and return the corresponding coverage object
def get_coverage () -> dict:

    # run coverage.py
    # are there something in windows like /tmp that is not ./tmp ???
    os.chdir('/tmp')
    
    sp.run("coverage run --branch -m pytest ", shell=True, check=True, capture_output=True)
    sp.run("coverage json --pretty-print -o cov.json", shell=True, check=True, capture_output=True)

    # get result
    result_file = open('cov.json', 'r')
    result_obj = json.load(result_file)
    result_file.close()

    assert('files' in result_obj.keys())
    assert('target.py' in result_obj['files'])

    return result_obj['files']['target.py']

def parse_coverage (cov) :
    stmt = (cov['summary']['num_statements'], cov['summary']['covered_lines'])
    branch = (cov['summary']['num_branches'], cov['summary']['covered_branches'])
    return stmt, branch

def test_dummy () :
    with open("testcases/dummy.py") as f:
        target_code = f.read()
    with open("testcases/dummy_test.py") as f:
        test_suite = f.read()

    make_target.write_target(target_code, test_suite)

    c = get_coverage()
    assert parse_coverage(c) == ((14, 14), (0, 0))

if __name__ == "__main__" :
    test_dummy()
