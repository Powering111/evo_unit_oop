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
    # are there something in windows like /tmp that is not ./tmp ???
    os.chdir('/tmp')
    
    sp.run("coverage run --branch -m pytest ", shell=True, check=True, capture_output=True)
    sp.run("coverage json --pretty-print -o cov.json", shell=True, check=True, capture_output=True)

    # get result
    result_file = open('cov.json', 'r')
    result_obj = json.load(result_file)
    result_file.close()

    assert ('files' in result_obj.keys())
    target_result = [file for file in result_obj['files'] if file.split('/')[-1] == 'target.py']
    assert len(target_result) == 1

    return result_obj['files'][target_result[0]]

def parse_coverage (cov) :
    stmt = (cov['summary']['num_statements'], cov['summary']['covered_lines'])
    branch = (cov['summary']['num_branches'], cov['summary']['covered_branches'])
    return stmt, branch
