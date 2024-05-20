# evo_unit_oop
Automated unit test generation for python classes, using evolutionary programming.

## Structure
- Place the targets and sample test suite in `testcases`
    - target should consist of only class definitions and import statements.
    - test suite should consist of test functions which does not get any parameter. They are automatically invoked.
- Fitness will be implemented in `fitness`
- Evoluationary algorithm will be implemented in `evolution`
- `main.py` to be realized and format later on :)

## Execution
Python 3.10 is required to run this application. 


To install dependencies, run
```
pip install -r requirements
```

To test evolutionary, run following(to be changed):
```
python evolution/evolution.py -t testcases/dummy.py
```

