from itertools import product

from dataclasses import dataclass
from pathlib import Path
from typing import Union, List

import mip

from models import WorkDay, Solution
from solver.helpers import (
    get_task_start_time_vector,
    get_task_finish_time_vector,
    get_worker_start_time_vector,
    get_worker_finish_time_vector,
    get_task_skillset_matrix,
    get_worker_skillset_matrix,
)


@dataclass
class ModelParameters:
    task_start_vector: List[int]
    task_finish_vector: List[int]
    task_skillset_matrix: List[int]
    worker_start_vector: List[int]
    worker_finish_vector: List[int]
    worker_skillset_matrix: List[int]


def load_work_day(file: Union[str, Path]) -> WorkDay:
    return WorkDay.parse_file(file)


def _remove_tasks_with_no_time(workday: WorkDay) -> WorkDay:
    # This is a work around while we still have tasks with no time
    return WorkDay(
        tasks=[task for task in workday.tasks if task.time is not ""],
        staff_members=workday.staff_members,
    )


def build_matrices(work_day: WorkDay) -> ModelParameters:
    return ModelParameters(
        task_start_vector=get_task_start_time_vector(work_day),
        task_finish_vector=get_task_finish_time_vector(work_day),
        worker_start_vector=get_worker_start_time_vector(work_day),
        worker_finish_vector=get_worker_finish_time_vector(work_day),
        worker_skillset_matrix=get_worker_skillset_matrix(work_day),
        task_skillset_matrix=get_task_skillset_matrix(work_day),
    )


def build_and_solve(
    work_day: WorkDay,
    model_parameters: ModelParameters,
) -> mip.Model:
    model = mip.Model("work-scheduler")

    n_workers = len(work_day.staff_members)
    n_tasks = len(work_day.tasks)

    # worker x task matrix
    worker_task_matrix = [
        [model.add_var(var_type=mip.BINARY) for _ in work_day.tasks]
        for _ in work_day.staff_members
    ]

    # task x worker matrix
    task_worker_matrix = list(zip(*worker_task_matrix))

    # Constraints

    # All tasks must be assigned
    for i in range(n_tasks):
        model += mip.xsum(task_worker_matrix[i]) == 1

    # Workers can only work on one task at a time
    for i in range(n_workers):
        model += mip.xsum(worker_task_matrix[i]) <= 1

    # Tasks can only have one worker assigned to them
    for i in range(n_tasks):
        model += mip.xsum(task_worker_matrix[i]) <= 1

    # Workers can only work on tasks that start after their start time
    for i, j in product(range(n_workers), range(n_tasks)):
        model += (
            worker_task_matrix[i][j] * model_parameters.worker_start_vector[i]
            - worker_task_matrix[i][j] * model_parameters.task_start_vector[j]
            <= 0
        )

    # Workers can only work on tasks that finish before their end time
    for i, j in product(range(n_workers), range(n_tasks)):
        model += (
            worker_task_matrix[i][j] * model_parameters.task_finish_vector[j]
            - worker_task_matrix[i][j] * model_parameters.worker_finish_vector[i]
            <= 0
        )

    # Workers need breaks (logic tbd, maybe ignore for prototype)
    # Workers can only work on tasks that they have the skills for

    # Objective

    # Evenly distribute tasks
    lowest_workload = model.add_var(name="lowest_workload")
    highest_workload = model.add_var(name="highest_workload")

    for i in range(n_workers):
        model += mip.xsum(worker_task_matrix[i]) <= highest_workload
        model += mip.xsum(worker_task_matrix[i]) >= lowest_workload

    model.objective = mip.minimize(highest_workload - lowest_workload)

    # TODO(j.swannack): Minimize high skilled workers doing "any" task

    model.optimize()

    allocations = []

    for i in range(n_workers):
        for j in range(n_tasks):
            if worker_task_matrix[i][j].x >= 0.99:
                allocations.append((work_day.staff_members[i], work_day.tasks[j]))

    return Solution(allocations=allocations)


def solve(work_day: WorkDay) -> Solution:
    model_parameters = build_matrices(work_day)
    return build_and_solve(work_day, model_parameters)


def main():
    # todo define relative day somewhere in the workday

    data_files = [
        "test_data/solver/workday_example_1.json",
        "test_data/solver/workday_example_2.json",
        "test_data/solver/workday_example_3.json",
    ]

    for data_file in data_files:
        work_day = load_work_day(data_file)
        work_day = _remove_tasks_with_no_time(work_day)
        solution = solve(work_day)
        output_file = Path(data_file).with_suffix(".out.json")
        Path(output_file).write_text(solution.json(indent=2))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
