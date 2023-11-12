# work-scheduler

## High level description

todo olivia

# Things to do

## Parsing Excel Sheets

There are several spreadsheets containing the relevant information required to formulate an instance of the problem

* Master Schedule
* Roster
* Floor Allocations

We need parsers for all of these sheets, that build a `WorkDay` model.

## Solving the Worker Allocation Problem

A program/function that takes in a `WorkDay`, and returns a `Solution`

Validity criteria needs to be met in the `Solution` object:
* Staff members can't do two things at once
* Staff members can't work outside their hours
* Staff members can't work on two floors on a given work day (okay?)
* More to come

Secondary objectives:
* Continuity of tasks per staff member
    * Staff member A should do task 1 for all patients in a morning
* Equal balancing of tasks

## Presenting the Solution

Display a `Solution` object in some way that a staff member can follow. Needs to be printable, ideally an excel sheet that can edited.
There needs to be a per staff member allocations

## Dependencies for the solver

`pip install pydantic mip jinja2 plotly`

## How to use the Solver

Use the `solver.pipeline.run_solver` function, i.e.:

```python
from solver.pipeline import run_solver

# You can get your work day from anywhere, but here's an example loading from a file
work_day = WorkDay.parse_file(input_file)

run_solver(
    work_day=work_day,
    output_dir="outputs/example_report",
    open_browser=True,
)
```
