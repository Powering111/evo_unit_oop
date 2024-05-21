import ast
import sys
import argparse
import random
import string
import time
import reproduction
from fitness.combine import fitness_score
# 1. scanner - Find attribute, method
# 2. function - attribute init
# 3. method call order
# 6. function - Create new generation
# 4. function - reproduce input reproduce
# 5. function - input mutation 
# 7. Compare between generations -> select

# Find class in target file and execute scanner
class ClassFinder(ast.NodeVisitor):
    def __init__(self):  
        self.classList = [] # list of ClassScanner
        
    def visit_ClassDef(self, node):
        newClass = ClassScanner().visit(node)
        self.classList.append(newClass)
        rand_newClass = lambda : RandomInit(newClass)
        setattr(RandomObject, f"rand_{newClass.name}", rand_newClass)

    def report(self):
        for cls in self.classList:
            cls.report()
        
# Get class attributes and methods
class ClassScanner():
    def __init__(self):
        self.name = ""
        self.attributes = dict() # dict[attribute name, attribute type]
        self.methods = dict() # dict[method name, dict[arg name, arg type]]

    def visit(self, node): 
        self.name = node.name
        for fundef in node.body:
            if isinstance(fundef, ast.FunctionDef):
                if fundef.name == '__init__':
                    self.visit_init(fundef)
                else:
                    self.visit_method(fundef)
        return self
    
    def visit_init(self, node):
        argdict = dict() # dict[arg name, arg type]
        for x in node.args.args[1:]:
            argdict[x.arg] = x.annotation.id
        for e in node.body:
            if isinstance(e, ast.Assign):
                attr_name = e.targets[0].attr
                if isinstance(e.value, ast.Name):
                    self.attributes[attr_name] = argdict[e.value.id]
                elif isinstance(e.value, ast.Call):
                    self.attributes[attr_name] = "functioncall"
                
    def visit_method(self, node):
        name = node.name
        argsDict = dict()
        for x in node.args.args[1:]:
            argsDict[x.arg] = x.annotation.id
        self.methods[name] = argsDict      

    def report(self):
        print("name", self.name)    
        print("attributes", self.attributes)
        print("methods", self.methods)

# method call code string 
class MethodCall():
    def __init__(self, method_name, *args, **kwargs):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
    def call_str(self):
        arg_list = []
        for arg in self.args:
            arg_list.append(str(arg))
        for key, val in self.kwargs.items():
            arg_list.append(f"{key}={val}")
        return f".{self.method_name}({', '.join(arg_list)})"
    
class Assertion():
    def __init__(self, methodcall, attr_name):
        self.MethodCall = methodcall
        self.attr = attr_name

# Test case for a class
class Genome(): #1:1 with an object
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_args = args
        self.init_kwargs = kwargs
        self.methodCall_lst = [] #(methodCall, int)
    def set_methodCall_lst(self, methodCall_lst):
        self.methodCall_lst = methodCall_lst
    def add_methodcall(self, methodcall:MethodCall, priority:int):
        self.methodCall_lst.append((methodcall, priority))

# Random object generator
class RandomObject():
    def rand_int():
        return random.randint(-sys.maxsize - 1, sys.maxsize)
    def rand_float():
        return random.uniform(-sys.maxsize - 1, sys.maxsize)
    def rand_str():
        return_str = random.choice(string.ascii_letters + string.digits)
        for i in range(100):
            if random.randint(0, 10)<9:
                return_str += random.choice(string.ascii_letters + string.digits)
            else:
                break
        return f'"{return_str}"'
    def rand_bool():
        return bool(random.randint(0, 1))

# Random sequence generator
def RandomSequence(maxnum):
    ret = [random.randint(0, maxnum-1)]
    while True:
        if random.randint(0, 1): # increase length by 50% chance
            ret.append(random.randint(0, maxnum-1))
        else:
            break
    return ret
    
# Generate random values for class attributes
def RandomInit(Class:ClassScanner):
    attrs = []
    for attr_name, attr_type in Class.attributes.items():
        attrs.append(getattr(RandomObject, f"rand_{attr_type}")())
    #instance = getattr(Class.object, Class.name)
    return attrs

# Generate MethodCall object with random values
def RandomMethodCall(Class:ClassScanner, method_name:str):
    method_args = Class.methods[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(f"obj_{Class.name}{i}")
        else:
            args.append(getattr(RandomObject, f"rand_{arg_type}")())
    return MethodCall(method_name, *args)

def generateGenomeList(classList):
    genomeList = []
    for classObj in classList:
        for i in range(5):
            genome = Genome(classObj.name, *RandomInit(classObj))
            num_methods = len(classObj.methods)
            for i in RandomSequence(num_methods*2+len(classObj.attributes)):
                priority = RandomObject.rand_int()
                if i < num_methods:
                    genome.add_methodcall(RandomMethodCall(classObj, list(classObj.methods)[i]), priority)
                elif i < num_methods*2:
                    rand_method_call =RandomMethodCall(classObj, list(classObj.methods)[i-num_methods])
                    genome.add_methodcall(Assertion(rand_method_call, None), priority)
                else:
                    genome.add_methodcall(Assertion(None, list(classObj.attributes)[i-2*num_methods]), priority)
            genomeList.append(genome)
    return genomeList

def buildTestFile(genomeList):    
    # Create Test file
    # Run `python evolution/evolution.py -t testcases/dummy.py`
    f = open("testcases/testsuites/"+target[10:-3]+"_test.py", "w")
    f.write("import pytest\n\n")
    f.write("import target\n")
    f.write(f"from {target[10:-3]} import *\n\n")
    f.write("def test_example():\n")
    all_methodCalls = []
    # write initializer in test_file and collect method lists
    for i, genome in enumerate(genomeList):
        f.write(f"    obj_{genome.class_name}{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n")
        for methodCall, priority in genome.methodCall_lst:
            all_methodCalls.append((i, methodCall, priority))
    all_methodCalls.sort(key=lambda tup: tup[2])
    # write method calls in test_file
    for i, methodCall, priority in all_methodCalls:
        if isinstance(methodCall, MethodCall):
            f.write(f"    obj_{genome.class_name}{i}{methodCall.call_str()}")
        elif isinstance(methodCall, Assertion):
            if methodCall.attr != None:
                f.write(f"    #assert obj_{genome.class_name}{i}.{methodCall.attr} == ")
            elif methodCall.MethodCall != None:
                f.write(f"    #assert obj_{genome.class_name}{i}{methodCall.MethodCall.call_str()} == ")
        f.write(f" # priority: {priority}\n")

def testCaseStr(genomeList):
    return_str = f"import pytest\n\nimport target\nfrom {target[10:-3]} import *\n\ndef test_example():\n"
    all_methodCalls = []
    # write initializer in test_file and collect method lists
    for i, genome in enumerate(genomeList):
        return_str += (f"    obj_{genome.class_name}{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n")
        for methodCall, priority in genome.methodCall_lst:
            all_methodCalls.append((i, methodCall, priority))
    all_methodCalls.sort(key=lambda tup: tup[2])
    # write method calls in test_file
    for i, methodCall, priority in all_methodCalls:
        if isinstance(methodCall, MethodCall):
            return_str += (f"    obj_{genome.class_name}{i}{methodCall.call_str()}")
        elif isinstance(methodCall, Assertion):
            if methodCall.attr != None:
                return_str += (f"    #assert obj_{genome.class_name}{i}.{methodCall.attr} == ")
            elif methodCall.MethodCall != None:
                return_str += (f"    #assert obj_{genome.class_name}{i}{methodCall.MethodCall.call_str()} == ")
        return_str += (f" # priority: {priority}\n")
    return return_str

def fitness(genomeList): ## not implemented yet
    #return fitness_score("".join(lines), testCaseStr(genomeList))
    return 1


def evolve(finder:ClassFinder, threshold_score, max_generation):
    genomeList = generateGenomeList(finder.classList)
    prev_fitness = fitness(genomeList)
    for i in range(max_generation):
        print(prev_fitness)
        if prev_fitness >= threshold_score:
            return genomeList
        newgenList = reproduction.generate_newgen(genomeList)
        new_fitness = fitness(newgenList)
        if new_fitness > prev_fitness:
            genomeList = newgenList
            prev_fitness = new_fitness
    print(prev_fitness)
    return genomeList


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    target = args.target
    sys.argv[1:] = args.remaining
    print("sys argv", sys.argv[1:])

    lines = (open(target, "r").readlines())
    root = ast.parse("".join(lines), target)

    # print(ast.dump(root, include_attributes=False, indent=2))   
    finder = ClassFinder()
    finder.visit(root)
    finder.report()

    genomeList = evolve(finder, 3, 1)
    print(genomeList)
    buildTestFile(genomeList)