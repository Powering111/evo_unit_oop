import ast
import sys
import argparse
import os


class StaticAnalyzer():
    def __init__(self, stmt, branch):
        self.stmt = stmt
        self.branch = branch
    def visit(self, node, i):
        #print(i, node.__class__.__name__)
        if isinstance(node, (ast.stmt, ast.ExceptHandler)):
            self.stmt.add(node.lineno)
        controlClass = ["If", "For", "While", "Try", "FunctionDef"]
        if node.__class__.__name__ in controlClass:
            method_name = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method_name)
            return visitor(node, i) 
        else :
            return self.generic_visit(node, i)  
    def generic_visit(self, node, i):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                if len(value) != 0 and isinstance(value[0], ast.stmt):
                    for j in range(len(value)-1):
                        self.visit(value[j], value[j+1].lineno)
                    self.visit(value[len(value)-1], i)
                else:    
                    for item in value:
                        if isinstance(item, ast.AST):
                            self.visit(item, i)
            elif isinstance(value, ast.AST):
                self.visit(value, i)
    def visit_If(self, node, i):
        self.generic_visit(node, i)
        start = node.lineno
        end1 = node.body[0].lineno
        self.branch.add((start, end1))
        if node.orelse == []:
            end2 = i
        else:
            end2 = node.orelse[0].lineno
        self.branch.add((start, end2))
    def visit_For(self, node, i):
        self.generic_visit(node, node.lineno)
        start = node.lineno
        end1 = node.body[0].lineno
        self.branch.add((start, end1))
        if node.orelse == []:
            end2 = i
        else:
            end2 = node.orelse[0].lineno
        self.branch.add((start, end2))
    def visit_While(self, node, i):
        self.generic_visit(node, node.lineno)
        start = node.lineno
        end1 = node.body[0].lineno
        self.branch.add((start, end1))
        if node.orelse == []:
            end2 = i
        else:
            end2 = node.orelse[0].lineno
        self.branch.add((start, end2))
    def visit_Try(self, node, i):
        self.generic_visit(node, i)
        if len(node.handlers) > 1:
            for i in range (len(node.handlers)-1):
                start = node.handlers[i].lineno
                end1 = node.handlers[i].body[0].lineno
                end2 = node.handlers[i+1].lineno
                self.branch.add((start, end1))
                self.branch.add((start, end2))
    def visit_FunctionDef(self, node, i):
        self.generic_visit(node, -node.lineno)

class Record():
    def __init__(self, branch):
        self.stmt_found = set()
        self.branch_found = set()
        self._branch = branch
        self.prev = 0
    def add(self, i):
        self.stmt_found.add(i)
        if (self.prev, i) in self._branch:
            self.branch_found.add((self.prev, i))
        self.prev =i
    def print(self):
        print("stmt found", self.stmt_found)
        print("branch found", self.branch_found)

class CodeModifier(ast.NodeTransformer):
    def visit(self, node):
        self.generic_visit(node)
        if isinstance(node, ast.stmt):
            myNode = ast.Expr(value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='record', ctx=ast.Load()),
                            attr='add',
                            ctx=ast.Load()),
                        args=[ast.Constant(value=node.lineno)],
                        keywords=[]))
            return [myNode, node]
        return node

if __name__ == '__main__':
    print("dumping started")
    parser = argparse.ArgumentParser(description='Rewrites programs.')
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()

    target = args.target
    sys.argv[1:] = args.remaining
    print("sys argv", sys.argv[1:])

    lines = (open(target, "r").readlines())
    root = ast.parse("".join(lines), target)
    #stmt= set()
    #branch = set()
    #visitor = StaticAnalyzer(stmt, branch)
    #visitor.visit(root, -1)
    
    #newRoot = CodeModifier().visit(root)
    #ast.fix_missing_locations(newRoot)
    #print(f"stmt count: {len(stmt)}")
    #print(f"branch count: {len(branch)}")
    #print(stmt)
    #print(branch)
    print("-----------------------")
    #modified = ast.unparse(newRoot)
    #print(modified)
    print("-----------------------")
    #record = Record(branch)
    #exec(modified)
    #record.print()
    print(ast.dump(root, include_attributes=False, indent=4))
