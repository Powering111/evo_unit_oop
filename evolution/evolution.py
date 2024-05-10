import ast
import sys
import argparse

# 1. scan - attribute, method 찾는거
# 2. attribute init 함수
# 3. method 부르는 순서
# 4. input reproduce하는 함수
# 5. input mutation 함수
# 6. 새 generation 만드는 함수
# 7. generation끼리 비교-> 선택

class ClassFinder(ast.NodeVisitor):
    def __init__(self):
        self.classList = []
    def visit_ClassDef(self, node):
        self.classList.append(ClassScanner().visit(node))
    def report(self):
        for cls in self.classList:
            cls.report()

class ClassScanner():
    def __init__(self):
        self.name = ""
        self.attributes = dict() # attribute name - type
        self.methods = dict() # method name - dictionary of arguments

    def visit(self, node):
        self.name = node.name
        for fundef in node.body:
            if isinstance(fundef, ast.FunctionDef):
                if fundef.name == '__init__':
                    self.visit_init(fundef)
                self.visit_method(fundef)
        return self
    
    def visit_init(self, node):
        argdict = dict() # arg name - arg type
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
    
class Genome():
    def __init__(self, class_name, *args, **kwargs):
        self.class_name = class_name
        self.init_value = (args, kwargs)
        self.method_call_lst:list[MethodCall] = []
    def add_methodcall(self, methodcall:MethodCall):
        self.method_call_lst.add(methodcall)
    
    
class MethodCall():
    def __init__(self, method_name, *args, **kwargs):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
    def call_str(self):
        arg_str = ""
        for arg in self.args:
            arg_str += f"{arg}, "
        for key, val in self.kwargs.items():
            arg_str += f"{key}={val}, "
        return f".{self.method_name}({arg_str})"
    
gene1 = Genome("class1", arg1, arg2)
gene1.add_methodcall(MethodCall("methodname1"))

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

    print(ast.dump(root, include_attributes=False, indent=4))   

    finder = ClassFinder()
    finder.visit(root)
    finder.report()