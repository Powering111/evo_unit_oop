def test_create (): 
    c = Counter(5)
    assert c.report() == 5

def test_incr (): 
    c = Counter(8) 
    c.incr() 
    assert c.report() == 9

def test_decr (): 
    c = Counter(2) 
    c.decr() 
    assert c.report() == 1

def test_reset (): 
    c = Counter(4) 
    c.reset() 
    assert c.report() == 0
