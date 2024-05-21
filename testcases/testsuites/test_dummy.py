import target

def test_example():
    obj_Counter0 = target.Counter(3152078399374738590) 
    obj_Counter1 = target.Counter(5210355266588850666) 
    obj_Counter2 = target.Counter(1347878697796627844) 
    obj_Counter3 = target.Counter(-7050167503291574731) 
    obj_Counter4 = target.Counter(512026767525463950) 
    test0 = obj_Counter1.report()
    assert test0 == test0 # priority: -7346910006800419218
    test0 = obj_Counter2.report()
    assert test0 == test0 # priority: -7346910006800419218
    test0 = obj_Counter3.value
    assert test0 == test0 # priority: -931630550698093804
    test1 = obj_Counter2.report()
    assert test1 == test1 # priority: -399342935987954852
    test1 = obj_Counter3.report()
    assert test1 == test1 # priority: -399342935987954852
    test1 = obj_Counter2.report()
    assert test1 == test1 # priority: 2295572962659782946
    test1 = obj_Counter3.report()
    assert test1 == test1 # priority: 2295572962659782946
    obj_Counter4.incr() # priority: 6889964011784955863
    obj_Counter4.reset() # priority: 7782777829334499588
