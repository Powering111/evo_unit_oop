from . import fitness_cov, fitness_mut

def fitness_score () : 
    fitness = fitness_cov.coverage_score()
    time = 0
    print(fitness)

    if fitness > 1.5 : 
        fitness += fitness_mut.mutation_score()
        # get time  

    return (fitness, time)
