import target

def test_create():
    c = target.Counter(5)
    assert str(c.report()) == '5'

def test_incr():
    c = target.Counter(8)
    c.incr()
    assert str(c.report()) == '9'

def test_decr():
    c = target.Counter(2)
    c.decr()
    assert str(c.report()) == '1'

def test_reset():
    c = target.Counter(4)
    c.reset()
    assert str(c.report()) == '0'

def test_add():
    c1 = target.Counter(20)
    c2 = target.Counter(22)
    assert str(c1.report()) == '20'
    assert str(c2.report()) == '22'
    c3 = c1 + c2
    assert str(c3.report()) == '42'