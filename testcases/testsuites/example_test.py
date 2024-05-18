import pytest

import target
from example import *

def test_example():
    c0 = target.Counter(-2166184431931823494) 
    c0.report() 
    c0.reset() 
