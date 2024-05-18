import target

def test_create():
    r = target.Rectangle(1.5, 2.5, 3.5, 4.5)
    assert str(r) == 'Rect(1.5,2.5,3.5,4.5)'

def test_area():
    r = target.Rectangle(1.5, 2.0, 2.5, 3.0)
    assert str(r.area()) == '7.5'

def test_perimeter():
    r = target.Rectangle(1.5, 2.0, 2.5, 3.0)
    assert str(r.perimeter()) == '11.0'

def test_is_square():
    r = target.Rectangle(5, 6, 1, 1)
    assert str(r.is_square()) == 'True'

def test_eq():
    r1 = target.Rectangle(1, 2, 3, 4)
    r2 = target.Rectangle(2, 3, 4, 5)
    assert str(r1 == r2) == 'False'
