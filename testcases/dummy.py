class Counter : 
    def __init__ (self, v): 
        self.value = v

    def report (self): 
        return self.value

    def reset (self) : 
        self.value = 0

    def incr (self) : 
        self.value += 1

    def decr (self) : 
        self.value -= 1
