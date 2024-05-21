import pytest

import target
from dummynewgen import *

def test_example():
    obj_Counter0 = target.Counter(-661911887917457539, "c") 
    obj_Counter1 = target.Counter(-8073230767165188159, "DY") 
    obj_Counter2 = target.Counter(-8073230767165188159, "DY") 
    obj_Counter3 = target.Counter(-8073230767165188159, "DY") 
    obj_Counter4 = target.Counter(-661911887917457539, "c") 
    x = obj_Counter0.decr() # priority: -8010690821366723589
    assert(x==x)
    obj_Counter4.decr() # priority: -8010690821366723589
    obj_Counter1.reset() # priority: -4555967052708084969
    obj_Counter2.reset() # priority: -4555967052708084969
    obj_Counter3.reset() # priority: -4555967052708084969
    obj_Counter0.__add__(obj_Counter4) # priority: -4407043172786917969
    obj_Counter1.__add__(obj_Counter4) # priority: -4407043172786917969
    obj_Counter2.__add__(obj_Counter4) # priority: -4407043172786917969
    obj_Counter3.__add__(obj_Counter4) # priority: -4407043172786917969
    obj_Counter4.__add__(obj_Counter4) # priority: -4407043172786917969
    obj_Counter0.decr() # priority: -3418567506917610423
    obj_Counter4.decr() # priority: -3418567506917610423
    obj_Counter0.report() # priority: -2730098831554004329
    obj_Counter1.report() # priority: -2730098831554004329
    obj_Counter2.report() # priority: -2730098831554004329
    obj_Counter3.report() # priority: -2730098831554004329
    obj_Counter4.report() # priority: -2730098831554004329
    obj_Counter0.incr() # priority: -1834639328762816772
    obj_Counter4.incr() # priority: -1834639328762816772
    obj_Counter1.__add__(obj_Counter2) # priority: -1591098622738900143
    obj_Counter2.__add__(obj_Counter2) # priority: -1591098622738900143
    obj_Counter3.__add__(obj_Counter2) # priority: -1591098622738900143
    obj_Counter0.decr() # priority: 229268830882345272
    obj_Counter1.decr() # priority: 229268830882345272
    obj_Counter2.decr() # priority: 229268830882345272
    obj_Counter3.decr() # priority: 229268830882345272
    obj_Counter4.decr() # priority: 229268830882345272
    obj_Counter1.incr() # priority: 1696262241772076540
    obj_Counter2.incr() # priority: 1696262241772076540
    obj_Counter3.incr() # priority: 1696262241772076540
    obj_Counter0.reset() # priority: 5292722414086969424
    obj_Counter4.reset() # priority: 5292722414086969424
    obj_Counter0.incr() # priority: 7182739903459499786
    obj_Counter4.incr() # priority: 7182739903459499786
    obj_Counter1.decr() # priority: 8343065585963701826
    obj_Counter2.decr() # priority: 8343065585963701826
    obj_Counter3.decr() # priority: 8343065585963701826
