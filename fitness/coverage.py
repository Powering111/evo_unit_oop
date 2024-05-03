
# Given the target python class in string `target_code` and given the test-suite in string `test_suite`
# Run the coverage of the target code and test_suite

# Assuming that the format of the target class would be a file containing just one class and nothing else. 
# And the test suite would be a file containing just multiple functions and nothing else.

# Oh, would this path only works on unix? :(

import subprocess as sp
import json

def write_target (target_code, test_suite, path) : 
    with open (path, 'w') as f: 
        f.write(target_code) 
        f.write('\n')
        f.write(test_suite)

# TODO: is it correct?
def get_coverage (target_code, test_suite) :
    write_target(target_code, test_suite, "/tmp/target.py")
    
    sp.run("coverage run --branch /tmp/target.py", shell=True, check=True)
    sp.run("coverage json -o /tmp/cov.json", shell=True, check=True, capture_output=True)

    coverage = json.load(open("/tmp/cov.json"))
    return coverage

if __name__ == "__main__" : 
    target_code = "".join(open("../testcases/dummy.py").readlines())
    test_suite = "".join(open("../testcases/dummy_test.py").readlines())
    c = get_coverage(target_code, test_suite)
    print(c)

