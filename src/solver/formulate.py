from pathlib import Path
from typing import Union

from models import WorkDay
from solver.helpers import (
    get_task_start_time_vector,
    get_task_finish_time_vector,
    get_worker_start_time_vector,
    get_worker_finish_time_vector,
)


def load_work_day(file: Union[str, Path]) -> WorkDay:
    return WorkDay.parse_file(file)


def _remove_tasks_with_no_time(workday: WorkDay) -> WorkDay:
    # This is a work around while we still have tasks with no time
    return WorkDay(
        tasks=[task for task in workday.tasks if task.time is not ''],
        staff_members=workday.staff_members,
    )


def build_matrices(work_day: WorkDay):
    task_start_vector = get_task_start_time_vector(work_day)
    task_duration_vector = get_task_finish_time_vector(work_day)
    worker_start_vector = get_worker_start_time_vector(work_day)
    worker_end_vector = get_worker_finish_time_vector(work_day)

    # print them all
    print(
        f"task_start_vector: {task_start_vector}\n"
        f"task_duration_vector: {task_duration_vector}\n"
        f"worker_start_vector: {worker_start_vector}\n"
        f"worker_end_vector: {worker_end_vector}\n"
    )

    return (
        task_start_vector,
        task_duration_vector,
        worker_start_vector,
        worker_end_vector,
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
        work_day = _remove_tasks_with_no_time(work_day)
        build_matrices(work_day)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
