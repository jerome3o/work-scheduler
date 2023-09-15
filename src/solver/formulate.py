from pathlib import Path
from typing import Union

from models import WorkDay
from solver.helpers import (
    get_task_start_time_vector,
    get_task_duration_vector,
    get_worker_start_time_vector,
    get_worker_end_time_vector,
)

_DATA_FILE = "test_data/solver/workday.json"


def load_workday(file: Union[str, Path]) -> WorkDay:
    return WorkDay.parse_file(file)


def _remove_tasks_with_no_time(workday: WorkDay) -> WorkDay:
    # This is a work around while we still have tasks with no time
    return WorkDay(
        tasks=[
            task
            for task in workday.tasks
            if task.time is not None
        ],
        staff_members=workday.staff_members,
    )


def main():
    # todo define relative day somewhere in the workday

    workday = load_workday(_DATA_FILE)

    workday = _remove_tasks_with_no_time(workday)

    task_start_vector = get_task_start_time_vector(workday)
    task_duration_vector = get_task_duration_vector(workday)
    worker_start_vector = get_worker_start_time_vector(workday)
    worker_end_vector = get_worker_end_time_vector(workday)

    # print them all
    print(
        f"task_start_vector: {task_start_vector}\n"
        f"task_duration_vector: {task_duration_vector}\n"
        f"worker_start_vector: {worker_start_vector}\n"
        f"worker_end_vector: {worker_end_vector}\n"
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
