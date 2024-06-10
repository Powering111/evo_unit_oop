from fitness.settings import MUTATION_ALPHA
from . import fitness_cov, fitness_mut
from . import helper
from .settings import *
import numpy as np

def fitness_precombine (target_code: str, test_suite: str, verbose = False) -> list[float] :

    def log (*x) :
        if verbose : print(*x)

    helper.cleanup()
    helper.write_target(target_code, test_suite)
    try:
        helper.make_testsuite() 
    except helper.makeTestsuiteFailedException:
        return [0] # test suite creation failed due to infinite loop, runtime error, etc.

    if verbose: 
        print("Test suite made")
        c = fitness_cov.parse_coverage(fitness_cov.get_coverage())
        print("Coverage", c)
    
    fitness = fitness_cov.coverage_score() 
    fitness /= 2

    result = [fitness]

    length = max(1, len(test_suite) / 1000)
    log("length is", length, "k characters")

    if DO_MUTATION_TESTING : 
        m = fitness_mut.parse_mutation(fitness_mut.get_mutation())
        log("Mutation", m)

        (mut, _) = fitness_mut.mutation_score()
        result.append(mut)

    if DO_REC_LENGTH: 
        result.append(1/length)

    if DO_LENGTH: 
        result.append(length)

    return result

def fitness_score (*args, **kwargs) -> float :

    parts = fitness_precombine(*args, **kwargs)
    fitness = parts[0]
    index = 1

    if DO_MUTATION_TESTING : 
        fitness += MUTATION_ALPHA * parts[index]
        index += 1

    if DO_REC_LENGTH: 
        fitness += REC_LENGTH_ALPHA * parts[index]
        index += 1

    if DO_LENGTH: 
        fitness += LENGTH_ALPHA * parts[index]
        index += 1

    # sigmoid-like, normalizes to [0, 1)
    fitness = 2/(1 + np.exp(-fitness)) - 1
    return fitness

# Returns mapping from class name to the corresponding fitness.
# it only measures coverage.
def fitness_score_by_class(target_code: str, test_suite: str) -> dict[str,float]:

    helper.cleanup()
    helper.write_target(target_code, test_suite)
    helper.make_testsuite()

    return fitness_cov.coverage_by_class()
