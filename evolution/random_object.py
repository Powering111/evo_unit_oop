import random
import string
import sys
from collections import defaultdict

# Random object generator
class RandomObject():
    def __init__(self, object_count=defaultdict(int)):
        self.object_count = object_count
        self.prev_int = []
        self.prev_float = []
        self.prev_str = []

    def prev_or_new(self, type, randfunc):
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
        def randfunc(): return random.randint(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("int", randfunc)

    def rand_float(self):
        def randfunc(): return random.uniform(-sys.maxsize - 1, sys.maxsize)
        return self.prev_or_new("float", randfunc)

    def rand_str(self):
        def randfunc(): 
            return_str = random.choice(string.ascii_letters + string.digits)
            for _ in range(100):
                if random.randint(0, 10) < 9:
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
        while True:
            if random.randint(0, 1): # increase length by 50% chance
                ret.append(random.randint(0, maxnum-1))
            else:
                break
        return ret
    
    # Generate random values for class attributes
    def RandomInit(Class, rand_device) -> list:
        attrs = []
        for attr_name, attr_type in Class.attributes.items():
            attrs.append(getattr(rand_device, f"rand_{attr_type}")())
        # instance = getattr(Class.object, Class.name)
        return attrs