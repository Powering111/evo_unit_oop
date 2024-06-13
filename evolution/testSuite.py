from evolution.testCase import *
from evolution.scanner import ClassScanner

# Test suite is a collection of test cases.
class TestSuite():
    def __init__(self, is_unit: bool):
        self.is_unit = is_unit  # if false, it is pairwise testing test suite
        self.testCaselist = []

    def random_testCaseList(self, classlist: list[ClassScanner], classObj1: ClassScanner, classObj2: ClassScanner|None =None):
        if self.is_unit:
            self.testCaselist = generate_UnitTestCase_List(
                classlist, classObj1)
        else:
            self.testCaselist = generate_PairwiseTestCase_List(
                classlist, classObj1, classObj2)

    def build_testcases(self):
        if self.is_unit:
            return "import target\n" + build_UnitTestCases(self.testCaselist)
        else:
            return "import target\n" + build_PairwiseTestCases(self.testCaselist)

    def count_methodCalls(self):
        pass
