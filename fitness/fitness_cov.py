# Assuming that the format of the target class would be a file containing import statements and classes.
# And the test suite would be a file containing just multiple functions and nothing else.

import subprocess as sp
import json
import os
from . import helper
import pathlib
import ast

# Given the target python class in string `target_code` and given the test-suite in string `test_suite`
# Run the the test_suite and return the corresponding coverage object
def get_coverage () -> dict|None:

    # run coverage.py
    oldcwd = os.getcwd()
    os.chdir(helper.TMP_DIR)
    process = None
    try:
        if helper.USE_PYTEST:
            cmd=f"coverage run --branch -m pytest {helper.TEST_PATH}"
        else:
            cmd=f"coverage run --branch {helper.TEST_PATH}"

        process = sp.Popen(args=cmd.split(), stdout=sp.PIPE, stderr=sp.DEVNULL)
        process.wait(10)
    except sp.CalledProcessError:
        print("COVERAGE PROCESS ERROR")
        pass
    except sp.TimeoutExpired:
        print("timeout while measuring coverage")
        if process is not None:
            process.kill()
    try:
        sp.run("coverage json -o cov.json", shell=True, check=True, capture_output=False)
    except sp.CalledProcessError:
        print("COVERAGE JSON ERROR")
        os.chdir(oldcwd)
        return None
    # get result
    result_file = open('cov.json', 'r')
    result_obj = json.load(result_file)
    result_file.close()

    assert ('files' in result_obj.keys())
    target_result = [file for file in result_obj['files'] if file.split('/')[-1] == helper.TARGET_FILENAME]

    os.chdir(oldcwd)

    if len(target_result) != 1: 
        print("Coverage Result Not Found")
        return None
    return result_obj['files'][target_result[0]]

def parse_coverage (cov) :
    if cov is None:
        return None
    stmt = (cov['summary']['covered_lines'], cov['summary']['num_statements'])
    branch = (cov['summary']['covered_branches'], cov['summary']['num_branches'])
    return stmt, branch

class classLinenoScannerInner(ast.NodeVisitor):
    def __init__(self):
        self.data: set[int]=set()

    def generic_visit(self,node):
        if hasattr(node,'lineno'):
            self.data.add(node.lineno)
        ast.NodeVisitor.generic_visit(self,node)

# scans through class definition and return mapping from class name to list of linenos
class classLinenoScanner(ast.NodeVisitor):
    def __init__(self):
        self.data: dict[str,set[int]]={}
    
    def visit_ClassDef(self, node):
        self.data[node.name]=set()
        scannerInner = classLinenoScannerInner()
        for x in node.body:
            scannerInner.visit(x)
        self.data[node.name] = scannerInner.data
        
# mapping from class name to statement coverage of it
def coverage_by_class () -> dict[str,float]:
    # assuming the test suite is already copied to tmp
    coverage = get_coverage()

    target_code:str = (pathlib.Path(helper.TMP_DIR) / pathlib.Path(helper.TARGET_FILENAME)).read_text()
    target_root = ast.parse(target_code)
    
    scanner = classLinenoScanner()
    scanner.visit(target_root)
    
    covered_stmts = {}
    result = {}
    for className,linenos in scanner.data.items():
        assert len(linenos)>0
        covered_stmts[className]=0
        if coverage is not None:
            for lineno in coverage['executed_lines']:
                if lineno in linenos:
                    covered_stmts[className] += 1
            result[className] = covered_stmts[className]/len(linenos)
        else:
            result[className] = 0
    return result

def coverage_score () -> float: 
    c = parse_coverage(get_coverage())
    if c is None:
        return 0

    stmt_cov = c[0][0] / c[0][1] if c[0][1] != 0 else 1
    branch_cov = c[1][0] / c[1][1] if c[1][1] != 0 else 1

    return (stmt_cov + branch_cov)

