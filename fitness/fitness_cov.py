# Assuming that the format of the target class would be a file containing import statements and classes.
# And the test suite would be a file containing just multiple functions and nothing else.

import subprocess as sp
import json
import os
from . import helper

# Given the target python class in string `target_code` and given the test-suite in string `test_suite`
# Run the the test_suite and return the corresponding coverage object
def get_coverage () -> dict:

    # run coverage.py
    oldcwd = os.getcwd()
    os.chdir(helper.TMP_DIR)
    
    sp.run(f"coverage run --branch -m pytest {helper.TEST_PATH}", shell=True, check=True, capture_output=True)
    sp.run("coverage json --pretty-print -o cov.json", shell=True, check=True, capture_output=True)

    # get result
    result_file = open('cov.json', 'r')
    result_obj = json.load(result_file)
    result_file.close()

    assert ('files' in result_obj.keys())
    target_result = [file for file in result_obj['files'] if file.split('/')[-1] == helper.TARGET_FILENAME]
    assert len(target_result) == 1

    os.chdir(oldcwd)
    return result_obj['files'][target_result[0]]

def parse_coverage (cov) :
    stmt = (cov['summary']['covered_lines'], cov['summary']['num_statements'])
    branch = (cov['summary']['covered_branches'], cov['summary']['num_branches'])
    return stmt, branch

def coverage_score (): 
    c = parse_coverage(get_coverage())

    stmt_cov = c[0][0] / c[0][1] if c[0][1] != 0 else 1
    branch_cov = c[1][0] / c[1][1] if c[1][1] != 0 else 1

    return (stmt_cov + branch_cov)

