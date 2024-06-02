import os 
import ast
import shutil
import subprocess as sp
from .settings import *
import pathlib

def cleanup():
    # if os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR):
    #     shutil.rmtree(TMP_DIR)
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

def write_target (target_code: str, test_suite: str) : 
    (pathlib.Path(TMP_DIR) / TARGET_FILENAME).write_text(target_code)
    (pathlib.Path(TMP_DIR) / TEST_FILENAME).write_text(test_suite)

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

class makeTestsuiteFailedException(Exception): pass

# This rewrite the TEST_PATH as a result
def make_testsuite () :
    test_path = pathlib.Path(TEST_PATH)
    test_code = test_path.read_text()
    test_root = ast.parse(test_code)

    if DO_MUTATION_TESTING:
        oldcwd = os.getcwd()
        os.chdir(TMP_DIR)
        def instrument (node): 
            if not isinstance(node, ast.Assert) :           return node
            if not isinstance(node.test, ast.Compare):      return node 
            if not len(node.test.ops) == 1:                 return node 
            if not isinstance(node.test.ops[0], ast.Eq) :   return node
            if not len(node.test.comparators) == 1:         return node 
            rhs = node.test.comparators[0]

            node.test.left = ast.Call(ast.Name("pickle.dumps"), [node.test.left], [])
            node.test.comparators[0] = ast.Call(ast.Name(LOGGER_NAME), [rhs], [])
            return node

        test_root.body = walk(test_root.body, instrument)                         # type: ignore

        # TODO: this logger kinda assume the data to be string only
        logger = ast.parse(f"def {LOGGER_NAME} (x): x = pickle.dumps(x); print('{ASSERT_STR}', x); return x")

        with open ('instrument.py', 'w') as f: 
            f.write('import pickle\n\n')
            f.write(ast.unparse(logger))
            f.write('\n\n')
            f.write(ast.unparse(test_root))

        path = os.path.join(TMP_DIR, "instrument.py")
        try:
            result = sp.run(f"pytest -rP {path}", shell=True, check=True, capture_output=True, timeout=10)
        except sp.TimeoutExpired:
            os.chdir(oldcwd)
            raise makeTestsuiteFailedException
        except sp.CalledProcessError:
            os.chdir(oldcwd)
            raise makeTestsuiteFailedException

        lines = result.stdout.decode().split('\n')
        assert_lines = [' '.join(line.split(' ')[1:]) for line in lines if ASSERT_STR in line]
        
        def patch_result (node, results): 
            if not isinstance(node, ast.Assert) :           return node
            if not isinstance(node.test, ast.Compare):      return node 
            if not len(node.test.ops) == 1:                 return node 
            if not isinstance(node.test.ops[0], ast.Eq) :   return node
            if not len(node.test.comparators) == 1:         return node 

            result = results.pop(0)
            node.test.left = ast.Call(ast.Name('str'), [ast.Call(ast.Name("pickle.dumps"), [node.test.left], [])], [])
            node.test.comparators[0] = ast.Constant(result)
            return node

        test_code = open(TEST_PATH).read() # why read twice?
        test_root = ast.parse(test_code)
        test_root.body = walk(test_root.body, patch_result, assert_lines)             # type: ignore
        
        to_write = 'import pickle\n\n'
        to_write += ast.unparse(test_root)
        test_path.write_text(to_write)

        os.chdir(oldcwd)

    else:
        to_write = test_code+"\n\n"
        if not USE_PYTEST:
            for node in test_root.body:
                if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):
                    assert len(node.args.args)==0
                    to_write += f"{node.name}()\n"
        test_path.write_text(to_write)
    

