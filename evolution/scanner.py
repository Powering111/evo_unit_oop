import ast 
from collections import defaultdict
from evolution.random_object import RandomObject

# Find class in target file and execute scanner
class ClassFinder(ast.NodeVisitor):
    def __init__(self):  
        self.classList: list[ClassScanner] = []
        
    def visit_ClassDef(self, node):
        newClass = ClassScanner().visit(node)
        self.classList.append(newClass)
        # add rand_{class_name} method to RandomObject module 
        # so an instance of this class can be randomly generated
        setattr(RandomObject, f"prev_{newClass.name}", [])
        def rand_newClass(randself): 
            def randfunc():
                attrs = RandomObject.RandomInit(newClass, randself) ## maybe change to re-initialized random device
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