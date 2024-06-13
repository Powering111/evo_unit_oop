from fitness import fitness_cov, helper
import pathlib

target_code = pathlib.Path("testcases/student.py").read_text()
test_suite = pathlib.Path("testcases/testsuites/test_student.py").read_text()

helper.cleanup()
helper.write_target(target_code, test_suite)
helper.make_testsuite()

print(fitness_cov.coverage_by_class())