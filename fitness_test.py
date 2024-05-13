from fitness import fitness_cov, fitness_mut, helper, combine
import subprocess as sp
import os

def test_fitness_cov (expect) :
    c = fitness_cov.get_coverage()
    result = fitness_cov.parse_coverage(c)
    assert result == expect 
    print("Coverage tested")

def test_fitness_mut (expect) :
    r = fitness_mut.get_mutation()
    result = fitness_mut.parse_mutation(r)
    if expect: 
        assert result[:2] == expect[:2]
    else: 
        print("mutation:", result)
    print("Mutation tested")

def test_rewrite_target (oracle): 
    helper.make_testsuite()
    result = sp.run(f"diff {oracle} {helper.TEST_PATH}",
                    shell=True, capture_output=True)
    assert result.stdout.decode() == ""
    print("Rewriting Tested")

def test_dummy ():
    with open("testcases/dummy.py") as f:
        target_code = f.read()
    with open("testcases/dummy_test.py") as f:
        test_suite = f.read()

    helper.write_target(target_code, test_suite)

    test_rewrite_target("./testcases/dummy_test_oracle.py")
    test_fitness_cov(((15, 15), (0, 0)))
    test_fitness_mut((12, 12))
    print("Dummy File Tested")

    print(f'Combined: {combine.fitness_score(target_code, test_suite)}')

def test_rect ():
    with open("testcases/rect.py") as f:
        target_code = f.read()
    with open("testcases/rect_test.py") as f:
        test_suite = f.read()

    helper.write_target(target_code, test_suite)

    test_rewrite_target("./testcases/rect_test_oracle.py")
    test_fitness_cov(((27, 35), (2, 4)))
    test_fitness_mut(None) # It swings!
    print("Rect File Tested")

    print(f'Combined: {combine.fitness_score(target_code, test_suite)}')


if __name__ == "__main__" :
    os.chdir(os.path.dirname(__file__))
    test_dummy() # TAKES 10 seconds

    os.chdir(os.path.dirname(__file__))
    test_rect()  # TAKES 1 seconds
