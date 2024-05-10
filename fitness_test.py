from fitness import fitness_cov, fitness_mut, helper, combine
import subprocess as sp

def test_fitness_cov () :
    c = fitness_cov.get_coverage()
    assert fitness_cov.parse_coverage(c) == ((15, 15), (0, 0))
    print("Coverage tested")

def test_fitness_mut () :
    r = fitness_mut.get_mutation()
    result = fitness_mut.parse_mutation(r)
    assert result[0] == 12
    assert result[1] == 12
    print("Mutation tested")

def test_rewrite_target (): 
    helper.make_testsuite()
    result = sp.run("diff ./testcases/dummy_test_oracle.py /tmp/oop_test_gen/test_target.py",
                    shell=True, capture_output=True)
    assert result.stdout.decode() == ""
    print("Rewriting Tested")

def test_dummy ():
    with open("testcases/dummy.py") as f:
        target_code = f.read()
    with open("testcases/dummy_test.py") as f:
        test_suite = f.read()

    helper.write_target(target_code, test_suite)

    test_rewrite_target()
    test_fitness_cov()
    test_fitness_mut()
    print("Dummy File Tested")

    print(f'Combined: {combine.fitness_score(target_code, test_suite)}')


if __name__ == "__main__" :
    test_dummy()
