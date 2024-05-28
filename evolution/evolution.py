import ast
import sys
import random
import string
from evolution import reproduction
from fitness.combine import fitness_score

POP_SIZE = 5

# Find class in target file and execute scanner
class ClassFinder(ast.NodeVisitor):
    def __init__(self):  
        self.classList: list[ClassScanner] = []
        
    def visit_ClassDef(self, node):
        newClass = ClassScanner().visit(node)
        self.classList.append(newClass)
        def rand_newClass(): return RandomInit(newClass)
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
        for x in node.args.args[1:]:
            assert x.annotation is not None
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
        self.method_args[name] = argsDict  
        if isinstance(node.returns, ast.Name):
            self.method_return[name] = node.returns.id
        else:
            self.method_return[name] = "None"  

    def report(self):
        print(f"class {self.name}:\n  attributes")
        if len(self.attributes) == 0:
            print("    empty")
        else:
            for (name, type) in self.attributes.items():
                print(f"    {name}: {type}")

        print(f"  methods")
        if len(self.method_args) == 0:
            print("    empty")
        else:
            for (name, arg_type) in self.method_args.items():
                arg_str = ', '.join(
                    ['self']+[f'{name}: {type}' for (name, type) in arg_type.items()])
                print(f"    def {name}({arg_str}) -> {self.method_return[name]}")

    def is_empty(self) -> bool:
        if len(self.attributes) == 0 and len(self.method_args) == 0:
            return True
        else:
            return False


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
        self.methodCall_lst = [] #(methodCall/Assertion, int)
    def set_methodCall_lst(self, methodCall_lst):
        self.methodCall_lst = methodCall_lst

    def add_methodcall(self, methodcall, priority: int):
        self.methodCall_lst.append((methodcall, priority))

    def __str__(self):
        meta = f"genome for {self.class_name}: a={self.init_args} kw={self.init_kwargs}"
        gene = "\n\t".join(str(mc) for mc in self.methodCall_lst)
        return meta + '\n\t' + gene


# Random object generator
class RandomObject():
    def rand_int():
        return random.randint(-sys.maxsize - 1, sys.maxsize)

    def rand_float():
        return random.uniform(-sys.maxsize - 1, sys.maxsize)

    def rand_str():
        return_str = random.choice(string.ascii_letters + string.digits)
        for _ in range(100):
            if random.randint(0, 10) < 9:
                return_str += random.choice(string.ascii_letters +
                                            string.digits)
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
def RandomInit(Class: ClassScanner) -> list:
    attrs = []
    for attr_name, attr_type in Class.attributes.items():
        attrs.append(getattr(RandomObject, f"rand_{attr_type}")())
    # instance = getattr(Class.object, Class.name)
    return attrs


# Generate MethodCall object with random values
def RandomMethodCall(Class:ClassScanner, method_name:str):
    method_args = Class.method_args[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(f"obj_{Class.name}{i}")
        else:
            args.append(getattr(RandomObject, f"rand_{arg_type}")())
    return MethodCall(method_name, *args)

def sort_pop (pop) :
    return sorted(pop, key=lambda x: -x[1])

class Generation():
    def __init__(self, target_code: str):
        self.finder = ClassFinder()
        self.finder.visit(ast.parse(target_code))
        self.finder.report() # debug
        self.target_code = target_code

    def get_fitness(self, genomeList: list[Genome]) -> float:
        test_code = build_test(genomeList)
        score = fitness_score(self.target_code, test_code)
        return score

    def make_pop (self, pop) :
        fit = [self.get_fitness(p) for p in pop]
        return list(zip(pop, fit))

    def recalculate_fitness(self, pop): 
        pop = [p[0] for p in pop]
        fit = [self.get_fitness(p) for p in pop]
        return list(zip(pop, fit))

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        pop = generatePopulation(self.finder.classList)
        pop = self.make_pop(pop)
        # pop = sort_pop(pop)
        for _ in range(max_generation):
            pop = reproduction.generate_newgen(pop)
            pop = reproduction.mutate(pop)
            pop = self.recalculate_fitness(pop)
            pop = sort_pop(pop)
            pop = pop[:POP_SIZE]

            print("leading fitness: ", pop[0][1])

            if pop[0][1] > threshold_score : break


        return pop[0][0]

def generateGenomeList(classList):
    genomeList = []
    for classObj in classList:
        # don't consider empty class
        if classObj.is_empty():
            continue

        for i in range(5):
            genome = Genome(classObj.name, *RandomInit(classObj))
            num_methods = len(classObj.method_args)
            for i in RandomSequence(num_methods+len(classObj.attributes)):
                priority = RandomObject.rand_int()
                if i < num_methods:
                    if list(classObj.method_return.values())[i] != None:
                        rand_method_call =RandomMethodCall(classObj, list(classObj.method_args)[i])
                        genome.add_methodcall(Assertion(rand_method_call, None), priority)
                    else:
                        genome.add_methodcall(RandomMethodCall(classObj, list(classObj.method_args)[i]), priority)
                else:
                    genome.add_methodcall(Assertion(None, list(classObj.attributes)[i-num_methods]), priority)
            genomeList.append(genome)
    return genomeList

def generatePopulation (arg):
    return [generateGenomeList(arg) for _ in range(POP_SIZE)]

def build_test(genomeList):
    return_str = f"import target\n\ndef test_example():\n"
    all_methodCalls = []
    # write initializer and collect method lists
    for i, genome in enumerate(genomeList):
        return_str += (f"    obj_{genome.class_name}{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n")
        for methodCall, priority in genome.methodCall_lst:
            all_methodCalls.append((i, methodCall, priority))
    all_methodCalls.sort(key=lambda tup: tup[2])

    # write method calls in test_file
    count = 0
    for i, methodCall, priority in all_methodCalls:
        if isinstance(methodCall, MethodCall):
            return_str += (f"    obj_{genome.class_name}{i}{methodCall.call_str()}")
        elif isinstance(methodCall, Assertion):
            if methodCall.attr != None:
                return_str += (f"    test{count} = obj_{genome.class_name}{i}.{methodCall.attr}\n")
                return_str +=(f"    assert test{count} == test{count}")
                count +=1
            elif methodCall.MethodCall != None:
                return_str += (f"    test{count} = obj_{genome.class_name}{i}{methodCall.MethodCall.call_str()}\n")
                return_str +=(f"    assert test{count} == test{count}")
        return_str += (f" # priority: {priority}\n")
    return return_str

def run_evolution(target_code: str, threshold_score: float = 0.8, max_generation: int = 10) -> str:

    genomeList = Generation(target_code).evolve(threshold_score, max_generation)
    test_code = build_test(genomeList)

    return test_code
