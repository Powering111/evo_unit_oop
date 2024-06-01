from . import fitness_cov, fitness_mut
from . import helper

def fitness_score (target_code: str, test_suite: str, verbose = False) -> float :

    def log (*x) :
        if verbose : print(*x)

    helper.cleanup()
    helper.write_target(target_code, test_suite)
    try:
        helper.make_testsuite() 
    except helper.makeTestsuiteFailedException:
        return 0 # test suite creation failed due to infinite loop, runtime error, etc.
    
    log("Test suite made")
    c = fitness_cov.parse_coverage(fitness_cov.get_coverage())
    log("Coverage", c)
    
    fitness = fitness_cov.coverage_score() 
    time = None

    if fitness > 1.5 : 
        log("Doing mutation")
        m = fitness_mut.parse_mutation(fitness_mut.get_mutation())
        log("Mutation", m)

        (mut, time) = fitness_mut.mutation_score()
        fitness += mut

    length = max(1, len(test_suite) / 1000)
    log("length is", length, "k characters")

    fitness /= 3

    log("fitness: ", fitness)
    return fitness

