import os 
import subprocess as sp
from . import helper

def get_mutation ():
    # run mutatest
    os.chdir(helper.TMP_DIR)
    result = sp.run(f"mutatest -s ./target.py -t 'pytest {helper.TEST_FILENAME}'", shell=True, check=True, capture_output=True)
    return result.stdout.decode()

def parse_mutation (response) :
    lines = response.split('\n')
    detected = [line for line in lines if "DETECTED: " in line]
    total_run = [line for line in lines if "TOTAL RUNS: " in line]

    assert len(detected) == 1
    assert len(total_run) == 1

    return (int(detected[0].split()[-1]), int(total_run[0].split()[-1]))
