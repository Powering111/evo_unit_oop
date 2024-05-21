# dummy test case which has some branches

class class1:
    def __init__(self):
        pass

    def f1(self, arg1:int)->bool:
        if arg1>0:
            return True
        else:
            return False
    
    def f2 (self, arg1:int, arg2:int)->str:
        if arg1*arg2==0:
            return "one of them are 0"
        elif arg1+arg2==0:
            return "Sum is 0"
        elif arg1==arg2:
            return "Same"
        else:
            return "I don't know"

    def f3 (self, arg1:int):
        if arg1>0:
            for x in range(arg1):
                pass
    
    def f4 (self, arg1:int, arg2:int):
        if arg1>0:
            for x in range(arg1):
                if x >= arg2:
                    break
    