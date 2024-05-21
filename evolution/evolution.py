import ast
import sys
import random
import string
from . import reproduction
from fitness import combine as fitness
# 1. scanner - Find attribute, method
# 2. function - attribute init
# 3. method call order
# 6. function - Create new generation
# 4. function - reproduce input reproduce
# 5. function - input mutation
# 7. Compare between generations -> select


# Find class in target file and execute scanner
class ClassFinder(ast.NodeVisitor):
    def __init__(self, target_code: str):
        self.classList: list[ClassScanner] = []

        root = ast.parse(target_code)
        self.visit(root)
        self.report()

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
        self.name: str = ""
        # dict[attribute name, attribute type]
        self.attributes: dict[str, str] = dict()
        # dict[method name, (dict[arg name, arg type],return type)]
        self.methods: dict[str, tuple[dict[str, str], str]] = dict()

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

        # return type
        return_type = 'None'
        if node.returns is not None:
            return_type = node.returns.id
        self.methods[name] = (argsDict, return_type)

    def report(self):
        print(f"class {self.name}:\n  attributes")
        if len(self.attributes) == 0:
            print("    empty")
        else:
            for (name, type) in self.attributes.items():
                print(f"    {name}: {type}")

        print(f"  methods")
        if len(self.methods) == 0:
            print("    empty")
        else:
            for (name, (arg_type, return_type)) in self.methods.items():
                arg_str = ', '.join(
                    ['self']+[f'{name}: {type}' for (name, type) in arg_type.items()])
                print(f"    def {name}({arg_str}) -> {return_type}")

    def is_empty(self) -> bool:
        if len(self.attributes) == 0 and len(self.methods) == 0:
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

    __repr__ = call_str


# Test case for a class
class Genome():
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_args = args
        self.init_kwargs = kwargs
        self.methodCall_lst: list[tuple[MethodCall, int]] = []

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
def RandomSequence(maxnum: int) -> list[int]:
    ret = [random.randint(1, maxnum)]
    while True:
        if random.randint(0, 1):  # increase length by 50% chance
            ret.append(random.randint(1, maxnum))
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
def RandomMethodCall(Class: ClassScanner, method_name: str):
    (method_args, return_type) = Class.methods[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(f"obj_{Class.name}{i}")
        else:
            args.append(getattr(RandomObject, f"rand_{arg_type}")())
    return MethodCall(method_name, *args)


def generateGenomeList(classList: list[ClassScanner]) -> list[Genome]:
    genomeList: list[Genome] = []
    for classObj in classList:
        # don't consider empty class
        if classObj.is_empty():
            continue

        for i in range(5):
            genome = Genome(classObj.name, *RandomInit(classObj))
            for methodName in classObj.methods.keys():
                priority = RandomObject.rand_int()
                genome.add_methodcall(RandomMethodCall(
                    classObj, methodName), priority)
            genomeList.append(genome)
    return genomeList


# create test python script from the given genome list
def build_test(genomeList: list[Genome]) -> str:
    test_code = f"""
import pytest
import target

def test_example():
"""
    all_methodCalls = []
    # write initializer and collect method lists
    for i, genome in enumerate(genomeList):
        test_code += f"    obj_{genome.class_name}{i} = target.{genome.class_name}({', '.join(str(arg) for arg in genome.init_args)}) \n"
        for methodCall, priority in genome.methodCall_lst:
            all_methodCalls.append((i, methodCall, priority))
    all_methodCalls.sort(key=lambda tup: tup[2])

    # write method calls
    for i, methodCall, priority in all_methodCalls:
        test_code += f"    obj_{genome.class_name}{i}{methodCall.call_str()}"
        test_code += f" # priority: {priority}\n"

    return test_code


# abstraction of the entire generation
class Generation():
    def __init__(self, target_code: str):
        self.finder = ClassFinder(target_code)
        self.target_code = target_code

    def get_fitness(self, genomeList: list[Genome]) -> float:
        test_code = build_test(genomeList)
        score = fitness.fitness_score(self.target_code, test_code)
        return score

    def evolve(self, threshold_score: float, max_generation: int) -> list[Genome]:
        genomeList = generateGenomeList(self.finder.classList)
        prev_fitness = self.get_fitness(genomeList)
        for _ in range(max_generation):
            print(f"fitness: {prev_fitness}")
            if prev_fitness >= threshold_score:
                return genomeList
            newgenList = reproduction.generate_newgen(genomeList)
            newgenList = reproduction.mutate(newgenList)
            new_fitness = self.get_fitness(newgenList)
            if new_fitness > prev_fitness:
                genomeList = newgenList
                prev_fitness = new_fitness
        print(prev_fitness)
        return genomeList


# For example, run `python evolution/evolution.py -t testcases/dummy.py`
# run actual evolution and
def run_evolution(target_code: str) -> str:

    genomeList = Generation(target_code).evolve(0.95, 20)
    test_code = build_test(genomeList)

    return test_code
