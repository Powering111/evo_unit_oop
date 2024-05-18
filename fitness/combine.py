from . import fitness_cov, fitness_mut
from . import helper

def fitness_score (target_code: str, test_suite: str) -> tuple[float, float|None] :
    helper.cleanup()
    helper.write_target(target_code, test_suite)
    helper.make_testsuite() # TODO: verify

    fitness = fitness_cov.coverage_score()

    # we can also use len(test_suite) cause some are unreasonable long / contain duplicate tests
    
    time = None
    if fitness > 1.5 : 
        (mut, time) = fitness_mut.mutation_score()
        fitness += mut

    length = len(test_suite)
    fitness = fitness / 3

    return (fitness, time)

    # HOW do we combine time and fitness
    # (0.89, 5) should be better than (0.9, 1000) ?
    # What about 1 - (1 - fit)^(1 / time)
    # the reasoning for the formula is that if we have infinitely many random tests with score `0.89`, 
    # with equal time (1000) we will get more coverage when running `0.89` 200 times than `0.9` 1 time.

    # ENSURE time and length >= 1

    return 1 - (1 - fitness)**(1/time)
    return 1 - (1 - fitness)**(1/length)
    return 1 - (1 - fitness)**(1/sqrt(time * length))

