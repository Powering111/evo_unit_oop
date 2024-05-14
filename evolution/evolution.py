import ast
import sys
import argparse
import random
import secrets
import string
import reproduction
# 1. scanner - Find attribute, method
# 2. function - attribute init
# 3. method call order
# 6. function - Create new generation
# 4. function - reproduce input reproduce
# 5. function - input mutation 
# 7. Compare between generations -> select

# Find class and execute scanner
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
        print(self.name)    
        print(self.attributes)
        print(self.methods)

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

# Test suite for a class
class Genome():
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_args = args
        self.init_kwargs = kwargs
        self.methodCall_lst:list[MethodCall] = []
    def set_methodCall_lst(self, methodCall_lst):
        self.methodCall_lst = methodCall_lst
    def add_methodcall(self, methodcall:MethodCall):
        self.methodCall_lst.append(methodcall)

# Random object generator
class RandomObject():
    def rand_int():
        return random.randint(-sys.maxsize - 1, sys.maxsize)
    def rand_float():
        return random.uniform(-sys.maxsize - 1, sys.maxsize)
    def rand_str():
        strlen = random.randint(1, 100)
        return ''.join(secrets.choice(string.ascii_letters, string.digits) for i in range(strlen))
    def rand_bool():
        return bool(random.randint(0, 1))

# Random sequence generator
def RandomSequence(maxnum):
    ret = [random.randint(1, maxnum)]
    while True:
        if random.randint(0, 1): # increase length by 50% chance
            ret.append(random.randint(1, maxnum))
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
    args = []
    for arg_name, arg_type in method_args.items():
        args.append(getattr(RandomObject, f"rand_{arg_type}")())
    return MethodCall(method_name, *args)

def generateGenomeList(classList):
    genomeList = []
    for classObj in classList:
        genome = Genome(classObj.name, *RandomInit(classObj))
        for methodName in classObj.methods.keys():
            genome.add_methodcall(RandomMethodCall(classObj, methodName))
        genomeList.append(genome)
    return genomeList

def buildTestFile(targetName, genomeList):    
    # Create Test file
    # Run `python evolution/evolution.py -t testcases/dummy.py`
    f = open("testcases/testsuites/"+targetName+"_test.py", "w")
    f.write("import pytest\n\n")
    f.write("import target\n")
    f.write(f"from {targetName} import *\n\n")
    f.write("def test_example():\n")
    for i, genome in enumerate(genomeList):
        # initialize class object
        f.write(f"    c{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n")
        # call methods
        for methodCall in genome.methodCall_lst:
            f.write(f"    c{i}{methodCall.call_str()} \n")

# m = MethodCall("method1", 4, 5, val=5)
# print(m.call_str())

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

    x = RandomObject.rand_Counter()
    print(x)
    genomeList = generateGenomeList(finder.classList)
    buildTestFile(target[10:-3], genomeList)
    genomeList = reproduction.generate_newgen(genomeList)
    buildTestFile(target[10:-3]+"newgen", genomeList)