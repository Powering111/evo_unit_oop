import target

def test_create (): 
    c = target.Counter(5)
    assert c.report() == 5

def test_incr (): 
    c = target.Counter(8) 
    c.incr() 
    assert c.report() == 9

def test_decr (): 
    c = target.Counter(2) 
    c.decr() 
    assert c.report() == 1

def test_reset (): 
    c = target.Counter(4) 
    c.reset() 
    assert c.report() == 0

def test_add ():
    c1 = target.Counter(20)
    c2 = target.Counter(22)
    assert c1.report() == 20
    assert c2.report() == 22
    c3 = c1 + c2
    assert c3.report() == 42
