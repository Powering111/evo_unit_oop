import pytest

import target
from example import *

def test_example():
    c = target.Counter(0) 
    c.report() 
    c.reset() 
    c.__add__(c) 
