from itertools import product
from typing import List, Tuple
import logging

from pathlib import Path

import mip

from scheduler.models import (
    WorkDay,
    SolverOutput,
    TaskAllocation,
    TaskType,
    ModelValues,
    Solution,
    SolverInput,
)
from scheduler.solver.helpers import build_matrices, prepare_work_day, load_work_day
from scheduler.solver.model_parameters import ModelParameters

_logger = logging.getLogger(__name__)


START_BUFFER = 0


class InfeasibleException(Exception):
    pass


def build_and_solve(
    work_day: WorkDay,
    model_parameters: ModelParameters,
) -> Tuple[List[TaskAllocation], ModelValues]:
    model = mip.Model("work-scheduler")

    n_workers = len(work_day.staff_members)
    n_tasks = len(work_day.tasks)
    n_skills = len(list(TaskType))

    # worker x task matrix
    worker_task_matrix = [
        [
            model.add_var(name=f"{i},{j}", var_type=mip.BINARY)
            for i, _ in enumerate(work_day.tasks)
        ]
        for j, _ in enumerate(work_day.staff_members)
    ]

    # task x worker matrix
    task_worker_matrix = list(zip(*worker_task_matrix))

    # Constraints

    # All tasks must be assigned
    for i in range(n_tasks):
        model += mip.xsum(task_worker_matrix[i]) == 1

    # Workers can only work on one task at a time
    earliest_minute, latest_minute = model_parameters.get_time_range()
    for i in range(n_workers):
        for minute in range(earliest_minute, latest_minute):
            model += (
                mip.xsum(
                    [
                        worker_task_matrix[i][j]
                        for j in range(n_tasks)
                        if model_parameters.task_start_vector[j] <= minute
                        and model_parameters.task_finish_vector[j] >= minute
                    ]
                )
                <= 1
            )

    # Tasks can only have one worker assigned to them
    for i in range(n_tasks):
        model += mip.xsum(task_worker_matrix[i]) <= 1

    # Workers can only work on tasks that start after their start time
    for i, j in product(range(n_workers), range(n_tasks)):
        model += (
            worker_task_matrix[i][j] * model_parameters.worker_start_vector[i]
            - worker_task_matrix[i][j] * model_parameters.task_start_vector[j]
            <= -START_BUFFER
        )

    # Workers can only work on tasks that finish before their end time
    for i, j in product(range(n_workers), range(n_tasks)):
        model += (
            worker_task_matrix[i][j] * model_parameters.task_finish_vector[j]
            - worker_task_matrix[i][j] * model_parameters.worker_finish_vector[i]
            <= 0
        )

    # TODO(j.swannack): Workers need breaks (logic tbd, maybe ignore for prototype)

    # Workers can only work on tasks that they have the skills for
    for i, j in product(range(n_workers), range(n_tasks)):
        for skill_i in range(n_skills):
            if model_parameters.task_skillset_matrix[j][skill_i]:
                model += (
                    worker_task_matrix[i][j]
                    * model_parameters.worker_skillset_matrix[i][skill_i]
                    - worker_task_matrix[i][j]
                    * model_parameters.task_skillset_matrix[j][skill_i]
                    <= 0
                )

    # Objective

    # Evenly distribute tasks
    lowest_workload = model.add_var(name="lowest_workload")
    highest_workload = model.add_var(name="highest_workload")

    for i in range(n_workers):
        workload_duration = [
            worker_task_matrix[i][j]
            * (
                model_parameters.task_finish_vector[j]
                - model_parameters.task_start_vector[j]
            )
            for j in range(n_tasks)
        ]

        model += mip.xsum(workload_duration) <= highest_workload
        model += mip.xsum(workload_duration) >= lowest_workload

    model.objective = mip.minimize(highest_workload - lowest_workload)

    # TODO(j.swannack): Minimize high skilled workers doing "any" task

    result = model.optimize()

    if result != mip.OptimizationStatus.OPTIMAL:
        raise InfeasibleException(f"Unable to find optimal solution, status: {result}")

    allocations = []
    for i in range(n_workers):
        tasks = []
        for j in range(n_tasks):
            if worker_task_matrix[i][j].x >= 0.99:
                tasks.append(work_day.tasks[j])
        allocations.append(
            TaskAllocation(task=tasks, staff_member=work_day.staff_members[i])
        )

    return allocations


def solve(work_day: WorkDay) -> Solution:
    original_work_day = work_day.copy()

    work_day, infeasible_tasks = prepare_work_day(work_day)
    model_parameters = build_matrices(work_day)
    allocations = build_and_solve(work_day, model_parameters)
    return Solution(
        input=SolverInput(
            raw_work_day=original_work_day,
            processed_work_day=work_day,
        ),
        output=SolverOutput(
            allocations=allocations,
            infeasible_tasks=infeasible_tasks,
        ).dict(),
    )


def main():
    # todo define relative day somewhere in the workday

    data_files = [
        "test_data/solver/workday_example_1.json",
        "test_data/solver/workday_example_2.json",
        "test_data/solver/workday_example_3.json",
    ]

    for data_file in data_files:
        work_day = load_work_day(data_file)
        solution = solve(work_day)
        output_file = Path(data_file).with_suffix(".out.json")
        Path(output_file).write_text(solution.json(indent=2))

        break


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
