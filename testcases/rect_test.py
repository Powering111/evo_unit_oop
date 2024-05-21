import target 

def test_create () : 
    r = target.Rectangle(1.5, 2.5, 3.5, 4.5)
    assert r == r

def test_area () : 
    r = target.Rectangle(1.5, 2.0, 2.5, 3.0) 
    assert r.area() == r.area()

def test_perimeter () : 
    r = target.Rectangle(1.5, 2.0, 2.5, 3.0) 
    assert r.perimeter() == r.perimeter()

def test_is_square () : 
    r = target.Rectangle (5, 6, 1, 1)
    assert r.is_square() == r.is_square()

def test_eq () : 
    r1 = target.Rectangle(1, 2, 3, 4)
    r2 = target.Rectangle(2, 3, 4, 5)
    assert (r1 == r2) == (r1 == r2)
