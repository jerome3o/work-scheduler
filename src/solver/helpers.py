from typing import Union
from datetime import datetime
from pathlib import Path

from models import WorkDay, TaskType
from solver.model_parameters import ModelParameters


def _get_minutes_from_start_of_relative_date(
    time: datetime,
    relative_date: datetime = None,
) -> int:
    if relative_date is None:
        # get the start of the day
        relative_date = datetime(
            year=time.year,
            month=time.month,
            day=time.day,
        )

    return (time - relative_date).total_seconds() // 60


def get_task_start_time_vector(
    work_day: WorkDay,
    relative_date: datetime = None,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            task.time,
            relative_date=relative_date,
        )
        for task in work_day.tasks
    ]


def get_task_finish_time_vector(work_day: WorkDay) -> list:
    return [
        _get_minutes_from_start_of_relative_date(task.time) + task.duration
        for task in work_day.tasks
    ]


def get_worker_start_time_vector(
    work_day: WorkDay,
    relative_date: datetime = None,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            staff_member.shift.start_time,
            relative_date=relative_date,
        )
        for staff_member in work_day.staff_members
    ]


def get_worker_finish_time_vector(
    work_day: WorkDay,
    relative_date: datetime = None,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            staff_member.shift.finish_time,
            relative_date=relative_date,
        )
        for staff_member in work_day.staff_members
    ]


def get_worker_skillset_matrix(work_day: WorkDay) -> list:
    # This will be a one-hot encoding of the worker's skillset
    # With rows/cols being workers/skills
    return [
        [task_type in staff_member.attributes for task_type in TaskType]
        for staff_member in work_day.staff_members
    ]


def get_task_skillset_matrix(work_day: WorkDay) -> list:
    # This will be a one-hot encoding of the task's required skillset
    # With rows/cols being tasks/skills
    return [
        [task_type == task.required_attributes for task_type in list(TaskType)]

        # Change to this when/if required_attributes becomes a list
        # [task_type in task.required_attributes for task_type in list(TaskType)]
        for task in work_day.tasks
    ]


def build_matrices(work_day: WorkDay) -> ModelParameters:
    return ModelParameters(
        task_start_vector=get_task_start_time_vector(work_day),
        task_finish_vector=get_task_finish_time_vector(work_day),
        worker_start_vector=get_worker_start_time_vector(work_day),
        worker_finish_vector=get_worker_finish_time_vector(work_day),
        worker_skillset_matrix=get_worker_skillset_matrix(work_day),
        task_skillset_matrix=get_task_skillset_matrix(work_day),
    )

def load_work_day(file: Union[str, Path]) -> WorkDay:
    return WorkDay.parse_file(file)


def remove_tasks_with_no_time(workday: WorkDay) -> WorkDay:
    # This is a work around while we still have tasks with no time
    return WorkDay(
        tasks=[task for task in workday.tasks if task.time is not ""],
        staff_members=workday.staff_members,
    )
