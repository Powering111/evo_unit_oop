from . import fitness_cov, fitness_mut
from . import helper

def fitness_score (target_code: str, test_suite: str) -> float :
    helper.cleanup()
    helper.write_target(target_code, test_suite)
    try:
        helper.make_testsuite() # TODO: verify
    except helper.makeTestsuiteFailedException:
        return 0 # test suite creation failed due to infinite loop, runtime error, etc.
    
    fitness = fitness_cov.coverage_score()
    
    time = None
    if fitness > 1.5 : 
        (mut, time) = fitness_mut.mutation_score()
        fitness += mut
        # get time  

    # to be replaced to advanced algorithm later
    fitness /= 3
    if not time : 
        return fitness / 2
    return 1 - ((1 - fitness) ** (1.0 / time))
