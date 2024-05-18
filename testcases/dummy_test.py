import target

def test_create (): 
    c = target.Counter(5)
    assert str(c.report()) == str(c.report())

def test_incr (): 
    c = target.Counter(8) 
    c.incr() 
    assert str(c.report()) == str(c.report())

def test_decr (): 
    c = target.Counter(2) 
    c.decr() 
    assert str(c.report()) == str(c.report())

def test_reset (): 
    c = target.Counter(4) 
    c.reset() 
    assert str(c.report()) == str(c.report())

def test_add ():
    c1 = target.Counter(20)
    c2 = target.Counter(22)
    assert str(c1.report()) == str(c1.report())
    assert str(c2.report()) == str(c2.report())
    c3 = c1 + c2
    assert str(c3.report()) == str(c3.report())
