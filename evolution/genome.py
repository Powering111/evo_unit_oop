import random
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

# Generate MethodCall object with random values
def RandomMethodCall(Class, method_name:str, rand_device):
    method_args = Class.method_args[method_name]
    args = list()
    for arg_name, arg_type in method_args.items():
        if arg_type == "Self":
            i = random.randrange(0, 5)
            args.append(getattr(rand_device, f"rand_{Class.name}")())
        else:
            args.append(getattr(rand_device, f"rand_{arg_type}")())
    return MethodCall(Class.name, method_name, *args)

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