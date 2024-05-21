import os 
import ast
import shutil
import subprocess as sp
from .settings import *

def cleanup():
    # if os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR):
    #     shutil.rmtree(TMP_DIR)
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

def write_target (target_code: str, test_suite: str) : 
    oldcwd = os.getcwd()
    os.chdir(TMP_DIR)
    with open (TARGET_FILENAME, 'w') as f: 
        f.write(target_code) 
    with open(TEST_FILENAME, 'w') as f:
        f.write(test_suite)
    os.chdir(oldcwd)

def walk(node, mutator, *args):
    if isinstance(node, list) : 
        for i in range(len(node)) : 
            node[i] = mutator(walk(node[i], mutator, *args), *args)
        return node 

    if not hasattr(node, "_fields") : return node

    for key in node._fields : 
        attr = getattr(node, key)
        new_attr = mutator(walk(attr, mutator, *args), *args) 
        setattr(node, key, new_attr)

    return node

# This rewrite the TEST_PATH as a result
def make_testsuite () :
    oldcwd = os.getcwd()
    os.chdir(TMP_DIR)

    lines = open(TEST_FILENAME).readlines()
    root = ast.parse('\n'.join(lines))

    def instrument (node): 
        if not isinstance(node, ast.Assert) :           return node
        if not isinstance(node.test, ast.Compare):      return node 
        if not len(node.test.ops) == 1:                 return node 
        if not isinstance(node.test.ops[0], ast.Eq) :   return node
        if not len(node.test.comparators) == 1:         return node 
        rhs = node.test.comparators[0]

        node.test.comparators[0] = ast.Call(ast.Name(LOGGER_NAME), [rhs], [])
        return node

    root.body = walk(root.body, instrument)                         # type: ignore

    # TODO: this logger kinda assume the data to be string only
    logger = ast.parse(f"def {LOGGER_NAME} (x): print('{ASSERT_STR}', x); return x")

    with open ('instrument.py', 'w') as f: 
        f.write(ast.unparse(logger))
        f.write('\n\n')
        f.write(ast.unparse(root))

    path = os.path.join(TMP_DIR, "instrument.py")
    result = sp.run(f"pytest -rP {path}", shell=True, check=True, capture_output=True)
    lines = result.stdout.decode().split('\n')
    assert_lines = [' '.join(line.split(' ')[1:]) for line in lines if ASSERT_STR in line]
    
    def patch_result (node, results): 
        if not isinstance(node, ast.Assert) :           return node
        if not isinstance(node.test, ast.Compare):      return node 
        if not len(node.test.ops) == 1:                 return node 
        if not isinstance(node.test.ops[0], ast.Eq) :   return node
        if not len(node.test.comparators) == 1:         return node 

        result = results.pop(0)
        node.test.comparators[0] = ast.Constant(result)
        return node

    lines = open(TEST_PATH).readlines()
    root = ast.parse('\n'.join(lines))
    root.body = walk(root.body, patch_result, assert_lines)             # type: ignore

    with open (TEST_PATH, 'w') as f: 
        f.write(ast.unparse(root))
    
    os.chdir(oldcwd)

if __name__ == "__main__" :
    make_testsuite()
