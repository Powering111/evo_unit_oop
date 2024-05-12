from typing import Self

class Counter : 
    def __init__ (self, v: int): 
        self.value = v

    def report (self) -> int: 
        print(self.value)
        return self.value

    def reset (self) : 
        self.value = 0

    # def __add__ (self, other: Self) -> Self:
    #     return Counter(self.value + other.value)

    
c = Counter(10)