from . import fitness_cov, fitness_mut
from . import helper

def fitness_score (target_code: str, test_suite: str) -> float :
    helper.cleanup()
    helper.write_target(target_code, test_suite)
    fitness = fitness_cov.coverage_score()
    time = 0
    print(fitness)

    if fitness > 1.5 : 
        fitness += fitness_mut.mutation_score()
        # get time  

    return (fitness, time)
