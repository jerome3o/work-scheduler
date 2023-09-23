# Problem Formulation

A brain dump of our understanding of the problem so far.

## Problem Statement

We are trying to allocate tasks to workers, each task has:
* time
* duration
* required skillset
* ... exact details [here](src/models.py)

And each worker has a skillset, and a time availability i.e. start and end time of shift

Info on worker model also [here](src/models.py).

## Inputs

* List of workers
* List of tasks

## Constraints

* All tasks must be assigned
* Workers can only work on one task at a time
* Workers can only work on tasks that they have the skills for
* Workers can only work on tasks that are within their shift time
* Workers need breaks (logic tbd, maybe ignore for prototype)
* Tasks can only have one worker assigned to them

## Object Function

* Evenly distribute tasks
* Minimize high skilled workers doing "any" task

## Other notes

* Triplicates can be converted into a single task with a duration of 3x the original
* Tasks that require multiple workers can be converted into multiple tasks with the same duration and skillset requirements
* Potential solution for breaks: we add them as tasks.


## Rough plan

Construct a matrix of variables for workers and tasks, where each cell is a binary variable indicating whether a worker is assigned to a task.

Then we can add constraints to the matrix to enforce the constraints above.

Other vectors needed for:
* Tasks
  * Duration
  * Skillset
  * Start time
* Workers
  * Skillset
  * Start time
  * End time
