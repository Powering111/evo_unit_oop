import os 
import subprocess as sp
from . import helper

def get_mutation ():
    # run mutatest
    os.chdir('/tmp')
    result = sp.run("mutatest -s . -t pytest", shell=True, check=True, capture_output=True)
    return result.stdout.decode()

def test_dummy () :
    with open("testcases/dummy.py") as f:
        target_code = f.read()
    with open("testcases/dummy_test.py") as f:
        test_suite = f.read()

    helper.write_target(target_code, test_suite)

    c = get_mutation()
    print(c)
    # TO BE PARSED

if __name__ == "__main__" :
    test_dummy()
