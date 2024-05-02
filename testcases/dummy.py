class Counter : 
    pi = 3.14159
    print("hello world")
    def __init__ (self, v:int, s:str): 
        self.value = v
        self.strvalue = s

    def report (self) -> int: 
        print(self.value)
        return self.value

    def reset (self) : 
        self.value = 0

    def incr (self) : 
        self.value += 1

    def decr (self) : 
        self.value -= 1

class Counter2:
    def __init__(self, s:str, counter:Counter):
        self.s = s
        self.value = counter.report()
    def report(self):
        print(self.value)
    def report2(self, x:str):
        print(x)

x = Counter(10, "hfy")
y = Counter2("3fd", x)
y.report()
x.incr()
y.report()