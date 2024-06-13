from main import evolution
from fitness.combine import fitness_precombine
from fitness.settings import print_settings as print_fitness_settings
from evolution.settings import print_settings as print_evo_settings
import pathlib

if __name__ == "__main__": 

    target = "student.py"

    print_fitness_settings()
    print_evo_settings()
    print("###########################")
    for _ in range(10):
        evolution(pathlib.Path(f'./testcases/{target}'))
        code = open(f'./testcases/{target}').read()
        suite = open(f'./testcases/testsuites/test_{target}').read()
        fitness_precombine(code, suite, verbose=True)


