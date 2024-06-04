import random
import string
import sys
from collections import defaultdict
from copy import deepcopy
from typing import Any

# Random object generator
class RandomObject():
    def __init__(self, object_count:dict[Any, int]=defaultdict(int)):
        self.object_count = deepcopy(object_count)
        self.prev_int = []
        self.prev_float = []
        self.prev_str = []

    def prev_or_new(self, type, randfunc):
        # when random function is called, either previous values generated can be 
        # reused or a random value can be newly generated
        prev_list = getattr(self, f"prev_{type}")
        if self.object_count[type] != 0 and type not in ['int', 'float', 'str', 'bool']:
            rand_index = random.randint(1, self.object_count[type])
            return f"obj_{type}{rand_index}"
        rand_index = random.randint(0, len(prev_list))
        if rand_index == len(prev_list):
            new_value = randfunc()
            prev_list.append(new_value)
            return new_value
        else: 
            return prev_list[rand_index]

    def rand_int(self):
        def randfunc(): 
            if  bool(random.getrandbits(1)): 
                return random.randint(-100, 100)
            else:
                return random.randint(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("int", randfunc)

    def rand_float(self):
        def randfunc(): return random.uniform(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("float", randfunc)

    def rand_str(self):
        def randfunc(): 
            return_str = random.choice(string.ascii_letters)
            for _ in range(100):
                if random.random() < 0.9:
                    return_str += random.choice(string.ascii_letters +
                                                string.digits)
                else:
                    break
            return f'"{return_str}"'
        return self.prev_or_new("str", randfunc)

    def rand_bool(self):
        return bool(random.randint(0, 1))
    
# Random sequence generator
def RandomSequence(maxnum):
    ret = [random.randint(0, maxnum-1)]
    for _ in range(50):
        if random.randint(0, 1): # increase length by 50% chance
            ret.append(random.randint(0, maxnum-1))
        else:
            break
    return ret
    
# Generate random values for class attributes
def RandomInit(classobj, rand_device) -> list:
    attrs = []
    for attr_name, attr_type in classobj.attributes.items():
        attrs.append(getattr(rand_device, f"rand_{attr_type}")())
    # instance = getattr(Class.object, Class.name)
    return attrs
