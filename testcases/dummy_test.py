import target

def test_create (): 
    c = target.Counter(5, 'A')
    assert c == c

def test_incr (): 
    c = target.Counter(8, 'b') 
    c.incr() 
    assert c == c

def test_decr (): 
    c = target.Counter(2, 'c') 
    c.decr() 
    assert c == c

def test_reset (): 
    c = target.Counter(4, 'D') 
    c.reset() 
    assert c == c

def test_add ():
    c1 = target.Counter(20, 'e')
    c2 = target.Counter(22, 'Ef')
    assert c1 == c1
    assert c2 == c2
    c3 = c1 + c2
    assert c3 == c3
