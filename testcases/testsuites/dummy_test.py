import pytest

import target
from dummy import *

def test_example():
    c = target.Counter(0) 
    c.report() 
    c.reset() 
    c.incr() 
    c.decr() 
    c.__add__(c) 
