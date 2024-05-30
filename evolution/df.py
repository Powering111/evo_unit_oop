import ast
import sys
import random
import string
from collections import defaultdict
from evolution import reproduction
import pathlib
from fitness.combine import fitness_score

# Find class in target file and execute scanner
class ClassFinder(ast.NodeVisitor):
    def __init__(self):  
        self.classList = [] # list of ClassScanner
        
    def visit_ClassDef(self, node):
        newClass = ClassScanner().visit(node)
        self.classList.append(newClass)
        setattr(RandomObject, f"prev_{newClass.name}", [])
        def rand_newClass(randself): 
            def randfunc():
                attrs = RandomInit(newClass, randself) ## maybe change to re-initialized random device
                return f"target.{newClass.name}({",".join(str(x) for x in attrs)})"
            return getattr(randself, "prev_or_new")(newClass.name, randfunc)
        setattr(RandomObject, f"rand_{newClass.name}", rand_newClass)

    def report(self):
        for cls in self.classList:
            cls.report() 


# Get class attributes and methods
class ClassScanner(): 
    def __init__(self):
        self.name = ""
        self.attributes = dict() # dict[attribute name, attribute type]
        self.method_args = dict() # dict[method name, dict[arg name, arg type]]
        self.method_return = dict() # dict[method name, return type]
        self.required_object_count = defaultdict(int) #dict[type name, maximum required object for a method call]
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
        argdict: dict[str, str] = dict()  # dict[arg name, arg type]
        type_count = defaultdict(int)
        for x in node.args.args[1:]:
            assert x.annotation is not None
            argdict[x.arg] = x.annotation.id
            type_count[x.annotation.id] +=1
        for type in type_count:
            if type_count[type] > self.required_object_count[type]:
                self.required_object_count[type] = type_count[type]
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
        type_count = defaultdict(int)
        for x in node.args.args[1:]:
            argsDict[x.arg] = x.annotation.id
            type_count[x.annotation.id] +=1
        for type in type_count:
            if type_count[type] > self.required_object_count[type]:
                self.required_object_count[type] = type_count[type]
        self.method_args[name] = argsDict  
        if isinstance(node.returns, ast.Name):
            self.method_return[name] = node.returns.id
        else:
            self.method_return[name] = None    

    def report(self):
        print("name", self.name)    
        print("attributes", self.attributes)
        print("method_args", self.method_args)
        print("method_return", self.method_return)
        print("type_count:", self.required_object_count)


# method call code string


class MethodCall():
    def __init__(self, class_name, method_name, *args, **kwargs):
        self.method_name = method_name
        self.class_name = class_name
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
    def __init__(self, class_name, methodcall, attr_name):
        self.class_name = class_name
        self.MethodCall = methodcall
        self.attr = attr_name


# Test case for a class
class Genome(): #1:1 with an object
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_args = args
        self.init_kwargs = kwargs
        self.methodCall_lst = [] #(methodCall/Assertion, int)
    def set_methodCall_lst(self, methodCall_lst):
        self.methodCall_lst = methodCall_lst

    def add_methodcall(self, methodcall: MethodCall, priority: int):
        self.methodCall_lst.append((methodcall, priority))

    def __repr__(self):
        meta = f"genome for {self.class_name}: a={self.init_args} kw={self.init_kwargs}"
        gene = "\n\t".join(str(mc) for mc in self.methodCall_lst)
        return meta + '\n\t' + gene


# Random object generator
class RandomObject():
    def __init__(self):
        self.prev_int = []
        self.prev_float = []
        self.prev_str = []

    def prev_or_new(self, type, randfunc):
        
        prev_list = getattr(self, f"prev_{type}")
        rand_index = random.randint(0, len(prev_list))
        if rand_index == len(prev_list):
            new_value = randfunc()
            prev_list.append(new_value)
            return new_value
        else: 
            return prev_list[rand_index]

    def rand_int(self):
        def randfunc(): return random.randint(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("int", randfunc)

    def rand_float(self):
        def randfunc(): return random.uniform(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("float", randfunc)

    def rand_str(self):
        def randfunc(): 
            return_str = random.choice(string.ascii_letters + string.digits)
            for _ in range(100):
                if random.randint(0, 10) < 9:
                    return_str += random.choice(string.ascii_letters +
                                                string.digits)
                else:
                    break
            return f'"{return_str}"'
        return self.prev_or_new("str", randfunc)

    def rand_bool(self):
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
def RandomInit(Class: ClassScanner, rand_device: RandomObject) -> list:
    attrs = []
    for attr_name, attr_type in Class.attributes.items():
        attrs.append(getattr(rand_device, f"rand_{attr_type}")())
    # instance = getattr(Class.object, Class.name)
    return attrs


# Generate MethodCall object with random values
def RandomMethodCall(Class:ClassScanner, method_name:str, rand_device:RandomObject):
    method_args = Class.method_args[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(f"obj_{Class.name}{i}")
        else:
            args.append(getattr(rand_device, f"rand_{arg_type}")())
    return MethodCall(Class.name, method_name, *args)

class Generation():
    def __init__(self, target_code: str):
        self.finder = ClassFinder()
        self.finder.visit(ast.parse(target_code))
        self.finder.report()
        self.target_code = target_code

    def get_fitness(self, genomeList: list[Genome]) -> float:
        test_code = build_test(genomeList)
        #score = fitness.fitness_score(self.target_code, test_code)
        return 1

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        genomeList = generateGenomeList(self.finder.classList)
        prev_fitness = self.get_fitness(genomeList)
        for _ in range(max_generation):
            print(f"fitness: {prev_fitness}")
            if prev_fitness >= threshold_score:
                return genomeList
            newgenList = reproduction.generate_newgen(genomeList)
            reproduction.mutate(newgenList)
            new_fitness = self.get_fitness(newgenList)
            if new_fitness > prev_fitness:
                genomeList = newgenList
                prev_fitness = new_fitness
        print(f"fitness: {prev_fitness}")
        return genomeList

def generateGenomeList(classList):
    genomeList = []
    rand_device = RandomObject()
    for classObj in classList:
        # don't consider empty class
        for i in range(5):
            genome = Genome(classObj.name, *RandomInit(classObj, rand_device))
            num_methods = len(classObj.method_args)
            for i in RandomSequence(num_methods+len(classObj.attributes)):
                priority = random.randint(-sys.maxsize - 1, sys.maxsize)
                if i < num_methods:
                    if list(classObj.method_return.values())[i] != None:
                        rand_method_call =RandomMethodCall(classObj, list(classObj.method_args,)[i], rand_device)
                        genome.add_methodcall(Assertion(classObj.name, rand_method_call, None), priority)
                    else:
                        genome.add_methodcall(RandomMethodCall(classObj, list(classObj.method_args)[i], rand_device), priority)
                else:
                    genome.add_methodcall(Assertion(classObj.name, None, list(classObj.attributes)[i-num_methods]), priority)
            genomeList.append(genome)
    return genomeList

def build_test(genomeList):
    return_str = f"import target\n\ndef test_example():\n"
    all_methodCalls = []
    # write initializer and collect method lists
    for i, genome in enumerate(genomeList):
        return_str += (f"    obj_{genome.class_name}{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n")
        for methodCall, priority in genome.methodCall_lst:
            all_methodCalls.append((i, methodCall, priority))
            #print(i, methodCall.class_name)
    all_methodCalls.sort(key=lambda tup: tup[2])
    # write method calls in test_file
    count = 0

    for (i, methodCall, priority) in all_methodCalls:
        #print(i, methodCall.class_name)
        if isinstance(methodCall, MethodCall):
            return_str += (f"    obj_{methodCall.class_name}{i}{methodCall.call_str()}")
        elif isinstance(methodCall, Assertion):
            if methodCall.attr != None:
                return_str += (f"    test{count} = obj_{methodCall.class_name}{i}.{methodCall.attr}\n")
                return_str +=(f"    assert test{count} == test{count}")
                count +=1
            elif methodCall.MethodCall != None:
                return_str += (f"    test{count} = obj_{methodCall.class_name}{i}{methodCall.MethodCall.call_str()}\n")
                return_str +=(f"    assert test{count} == test{count}")
                count+=1
        return_str += (f" # priority: {priority}\n")
    return return_str

def run_evolution(target_code: str) -> str:

    genomeList = Generation(target_code).evolve(2, 1)
    test_code = build_test(genomeList)

    return test_code