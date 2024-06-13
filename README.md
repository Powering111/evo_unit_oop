# Automatic Test Case Generation for Object-Oriented Python Classes Using an Evolutionary Algorithm

### Introduction

This project presents an approach to automatically generating test cases for object-oriented Python classes using an evolutionary algorithm. The aim is to enhance the efficiency and coverage of unit tests, dynamically generating and evolving test cases based on their effectiveness, as measured by a custom fitness function.

### Features

- Automated Test Generation: Automatically generates test cases for Python classes.
- Evolutionary Algorithm: Utilizes genetic operations like selection, crossover, and mutation to evolve test cases.
- Fitness Function: Measures the effectiveness of test cases based on code coverage and mutation testing.
- Comprehensive Coverage: Supports both unit tests and pairwise tests to ensure thorough testing of class interactions.

## Structure

- Place the targets and sample test suite in `testcases`
  - target should consist of only class definitions and import statements.
  - test suite should consist of test functions which does not get any parameter. They are automatically invoked.
- Fitness will be implemented in `fitness`
- Evoluationary algorithm will be implemented in `evolution`
- `main.py` to be realized and format later on :)

## Installation

### Prerequisites

- Python 3.10
- Git

### Steps

1. Clone the repository:

```
git clone https://github.com/coinse-classroom/cs453-spring-2024-project-reports-lilble.git
cd evo_unit_oop
```

2. Install the required dependencies:

```
pip install -r requirements
```

## Usage

### Command Line Interface

To run the evolutionary algorithm on a target Python file, use the following command:

```
python main.py -t path_to_target_file.py
```

`-t`, `--target`: Path to the target Python file containing the class definitions. In this project, try example files in `testcases`.
