import os 
import subprocess as sp
from . import helper

def get_mutation ():
    # run mutatest
    os.chdir(helper.TMP_DIR)
    result = sp.run(f"mutatest -s ./{helper.TARGET_FILENAME} -t 'pytest {helper.TEST_PATH}' -r {helper.SEED}", 
                    shell=True, check=True, capture_output=True)
    return result.stdout.decode()

def parse_mutation (response) :
    lines = response.split('\n')
    detected = [line for line in lines if "DETECTED: " in line]
    total_run = [line for line in lines if "TOTAL RUNS: " in line]
    runtime = [line for line in lines if "total run time" in line]

    assert len(detected) == 1
    assert len(total_run) == 1

    if len(runtime) == 1: 
        runtime = runtime[0].split()[-1]
        hour, minute, second = runtime.split(':')
        runtime = int(hour) * 3600 + int(minute) * 60 + float(second)
    else: 
        runtime = None

    return (int(detected[0].split()[-1]), int(total_run[0].split()[-1]), runtime)

def mutation_score (): 
    m = parse_mutation(get_mutation())
    return (m[0] / m[1] if m[1] != 0 else 0), m[2]
