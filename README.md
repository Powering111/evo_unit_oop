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
Python 3.11 is required to run this application. 

To use Self type annotation, we need python>3.11.


To install dependencies, run
```
python3.11 -m pip install -r requirements
```
