from . import fitness_cov, fitness_mut
from . import helper

def fitness_score (target_code: str, test_suite: str) -> tuple[float, float|None] :
    helper.cleanup()
    helper.write_target(target_code, test_suite)
    helper.make_testsuite() # TODO: verify

    fitness = fitness_cov.coverage_score()
    
    time = None
    if fitness > 1.5 : 
        (mut, time) = fitness_mut.mutation_score()
        fitness += mut
        # get time  

    return (fitness, time) #finess: max3
