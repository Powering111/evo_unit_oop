import random

def pseudo_norm():
    """Generate a value between 1-100 in a normal distribution"""
    count = 10
    values =  sum([random.randint(1, 100) for x in range(count)])
    return round(values/count)
    
lst = []
for i in range(10000):
    lst.append(pseudo_norm())

print(lst)
count_lst = {i: 0 for i in range(100)}
for i in lst:
    count_lst[i] += 1

for i in range(10000):
    print(f"{i}: {"*"*count_lst[i]}")