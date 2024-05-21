import target
from dummy import *

def test_example():
    obj_Counter0 = target.Counter(-1821540566192708058) 
    obj_Counter1 = target.Counter(422694435618249840) 
    obj_Counter2 = target.Counter(-3537245983523873796) 
    obj_Counter3 = target.Counter(-5132033441691761023) 
    obj_Counter4 = target.Counter(5515960799161636144) 
    test0 = obj_Counter4.value
    assert test0 == test0 # priority: 5065423022722182684
    obj_Counter1.incr() # priority: 5142900202517921089
    test1 = obj_Counter2.value
    assert test1 == test1 # priority: 5491281006178630528
    obj_Counter1.incr() # priority: 6148249168825240285
    obj_Counter2.incr() # priority: 6148249168825240285
    test2 = obj_Counter1.value
    assert test2 == test2 # priority: 6216472239817350537
    test3 = obj_Counter2.value
    assert test3 == test3 # priority: 6216472239817350537
    test4 = obj_Counter4.__add__(obj_Counter0)
    assert test4 == test4 # priority: 8082116986205988416

