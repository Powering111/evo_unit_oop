from evolution.random_object import RandomObject
from evolution.genome import *
from evolution.scanner import ClassScanner
import sys
from collections import defaultdict

from evolution.settings import CASE_PER_SUITE

def add_random_methodcall_sequence(classObj, obj, rand_device):
    ### add random numbers of random methodcalls to obj 
    num_methods = len(classObj.method_args)
    num_attrs = len(classObj.attributes)
    for i in RandomObject.RandomSequence(num_methods+num_attrs):
        priority = random.randint(-sys.maxsize - 1, sys.maxsize)
        if i < num_methods:
            if list(classObj.method_return.values())[i] != None:
                rand_method_call =RandomMethodCall(classObj, list(classObj.method_args,)[i], rand_device)
                obj.add_methodcall(Assertion(classObj.name, rand_method_call, None), priority)
            else:
                obj.add_methodcall(RandomMethodCall(classObj, list(classObj.method_args)[i], rand_device), priority)
        else:
            obj.add_methodcall(Assertion(classObj.name, None, list(classObj.attributes)[i-num_methods]), priority)


class UnitTestCase():
    def __init__(self, main_obj:Genome, surrounding_objs: list[Genome]):
        '''
        main_obj: calls methods in the test function
        surrounding_objs: does not call methods in the test function
        '''
        self.main_obj = main_obj 
        self.surrounding_objs = surrounding_objs 

def generate_UnitTestCase_List(classList: list[ClassScanner], classObj: ClassScanner) -> list[UnitTestCase]:
    TestCaseList: list[UnitTestCase] = []
    required_sub_obj = classObj.required_object_count
    for _ in range(CASE_PER_SUITE):
        required_sub_obj[classObj.name]+=1
        rand_device = RandomObject(required_sub_obj)
        required_sub_obj[classObj.name]-=1
        #initialize main_obj for the testcase
        main_obj = Genome(classObj.name, *RandomObject.RandomInit(classObj, rand_device))
        add_random_methodcall_sequence(classObj, main_obj, rand_device)
        # initialize surrounding_objs for the testcase
        # surrounding_objs are made only when main_obj has a method that uses it as a parameter
        surr_objs: list[Genome] = []
        for classObject in classList:
            for _ in range(required_sub_obj[classObject.name]):
                new_obj = Genome(classObject.name, *RandomObject.RandomInit(classObject, rand_device)) 
                surr_objs.append(new_obj)
        newTestCase = UnitTestCase(main_obj, surr_objs)
        TestCaseList.append(newTestCase)
    return TestCaseList

def build_UnitTestCases(TestCaseList: list[UnitTestCase]) -> str:
    class_name = TestCaseList[0].main_obj.class_name
    return_str = f"### unit testing for {class_name}\n"
    for i, testCase in enumerate(TestCaseList, start=1):
        return_str += f"\ndef test_{class_name}{i}():\n"
        # initialization of main_obj 
        main_obj_name = f"obj_{class_name}1"
        return_str += (f"    {main_obj_name}"
            f"= target.{class_name}({', '.join(str(arg) for arg in testCase.main_obj.args)}) \n")
        index_count = defaultdict(lambda: 1)
        index_count[class_name] += 1
        methodCalls = []
        methodCalls.extend(testCase.main_obj.methodCall_lst)
        methodCalls.sort(key=lambda tup: tup[1])
        # initialization of surrounding_obj
        
        for surr_obj in testCase.surrounding_objs:
            return_str += (f"    obj_{surr_obj.class_name}{index_count[surr_obj.class_name]}" 
                f"= target.{surr_obj.class_name}({', '.join(str(arg) for arg in surr_obj.args)}) \n")
            index_count[surr_obj.class_name] += 1
        # call methods
        count = 0
        for (methodCall, priority) in methodCalls:
            if isinstance(methodCall, MethodCall):
                return_str += (f"    {main_obj_name}{methodCall.call_str()}")
            elif isinstance(methodCall, Assertion):
                if methodCall.attr != None:
                    return_str += (f"    test{count} = {main_obj_name}.{methodCall.attr}\n")
                    return_str +=(f"    assert test{count} == test{count}\n")
                    count +=1
                elif methodCall.MethodCall != None:
                    return_str += (f"    test{count} = {main_obj_name}{methodCall.MethodCall.call_str()}\n")
                    return_str +=(f"    assert test{count} == test{count}\n")
                    count+=1
    return return_str + "\n\n"


class PairwiseTestCase():
    def __init__(self, main_obj1:Genome, main_obj2:Genome, surrounding_objs: list[Genome]):
        '''
        main_obj1, main_obj2: calls methods in the test function
        surrounding_objs: does not call methods in the test function
        '''
        self.main_obj1 = main_obj1
        self.main_obj2 = main_obj2
        self.surrounding_objs = surrounding_objs

def generate_PairwiseTestCase_List(classList: list[ClassScanner], classObj1: ClassScanner, classObj2: ClassScanner) -> list[PairwiseTestCase]:

    TestCaseList: list[PairwiseTestCase] = []
    required_sub_obj = defaultdict(int)
    # merge required_object_count for class1 and class2
    for d in (classObj1.required_object_count, classObj2.required_object_count):
        for k, v in d.items():
            required_sub_obj[k] = max(required_sub_obj[k], v)
    for _ in range(CASE_PER_SUITE):
        required_sub_obj[classObj1.name]+=1
        required_sub_obj[classObj2.name]+=1
        rand_device = RandomObject(required_sub_obj)
        required_sub_obj[classObj1.name]-=1
        required_sub_obj[classObj2.name]-=1
        #initialize main_obj for the testcase
        main_obj1 = Genome(classObj1.name, *RandomObject.RandomInit(classObj1, rand_device))
        main_obj2 = Genome(classObj2.name, *RandomObject.RandomInit(classObj2, rand_device))
        add_random_methodcall_sequence(classObj1, main_obj1, rand_device)
        add_random_methodcall_sequence(classObj2, main_obj2, rand_device)
        # initialize surrounding_objs for the testcase
        # surrounding_objs are made only when main_obj has a method that uses it as a parameter
        surr_objs = []
        for classObject in classList:
            for _ in range(required_sub_obj[classObject.name]):
                new_obj = Genome(classObject.name, *RandomObject.RandomInit(classObject, rand_device)) 
                surr_objs.append(new_obj)
        newTestCase = PairwiseTestCase(main_obj1, main_obj2, surr_objs)
        TestCaseList.append(newTestCase)
    return TestCaseList

def build_PairwiseTestCases(TestCaseList: list[PairwiseTestCase]) -> str:
    class_name1 = TestCaseList[0].main_obj1.class_name
    class_name2 = TestCaseList[0].main_obj2.class_name
    return_str = f"### pairwise testing for {class_name1} and {class_name2}\n"
    for i, testCase in enumerate(TestCaseList, start=1):
        # declare function
        return_str += f"\ndef test_{class_name1}_{class_name2}{i}():\n" 
        index_count = defaultdict(lambda: 1) # track object names
        main_obj1_name = f"obj_{class_name1}1"
        index_count[class_name1] +=1
        main_obj2_name =  f"obj_{class_name2}{index_count[class_name2]}"
        index_count[class_name2] +=1
        # initialize main objects
        return_str += (f"    {main_obj1_name}" 
            f"= target.{class_name1}({', '.join(str(arg) for arg in testCase.main_obj1.args)}) \n")
        return_str += (f"    {main_obj2_name}" 
            f"= target.{class_name2}({', '.join(str(arg) for arg in testCase.main_obj2.args)}) \n")
        # sort method calls by priority
        all_methodCalls = []
        for methodCall, priority in testCase.main_obj1.methodCall_lst:
            all_methodCalls.append((main_obj1_name, methodCall, priority))
        for methodCall, priority in testCase.main_obj2.methodCall_lst:
            all_methodCalls.append((main_obj2_name, methodCall, priority))
        all_methodCalls.sort(key=lambda tup: tup[2])
        # initialize surrounding objects
        for surr_obj in testCase.surrounding_objs:
            return_str += (f"    obj_{surr_obj.class_name}{index_count[surr_obj.class_name]}" 
                f"= target.{surr_obj.class_name}({', '.join(str(arg) for arg in surr_obj.args)}) \n")
            index_count[surr_obj.class_name] += 1
        # call methods and write assertions
        count = 0
        for (main_obj_name, methodCall, priority) in all_methodCalls:
            if isinstance(methodCall, MethodCall):
                return_str += (f"    {main_obj_name}{methodCall.call_str()}")
            elif isinstance(methodCall, Assertion):
                if methodCall.attr != None:
                    return_str += (f"    test{count} = {main_obj_name}.{methodCall.attr}\n")
                    return_str +=(f"    assert test{count} == test{count}\n")
                    count +=1
                elif methodCall.MethodCall != None:
                    return_str += (f"    test{count} = {main_obj_name}{methodCall.MethodCall.call_str()}\n")
                    return_str +=(f"    assert test{count} == test{count}\n")
                    count+=1
    return return_str + "\n\n"


