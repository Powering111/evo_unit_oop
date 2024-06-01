from typing_extensions import Self

class Counter : 
    def __init__ (self, v: int, s:str): 
        self.value = v
        self.strvalue = s

    def report (self) -> int: 
        print(self.value)
        return self.value

    def reset (self) -> None: 
        self.value = 0

    def incr (self) : 
        self.value += 1

    def decr (self) : 
        self.value -= 1

    def __add__ (self, other: Self) -> Self:
        return Counter(self.value + other.value, self.strvalue)
