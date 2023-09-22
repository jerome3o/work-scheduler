import logging
from typing import Union, Tuple, List
from datetime import datetime
from pathlib import Path

from models import WorkDay, TaskType, InfeasibleTask
from solver.model_parameters import ModelParameters

_logger = logging.getLogger(__name__)


def _get_day_start(time: datetime) -> datetime:
    return datetime(
        year=time.year,
        month=time.month,
        day=time.day,
    )


def _get_minutes_from_start_of_relative_date(
    time: datetime,
    relative_date: datetime,
) -> int:
    return (time - relative_date).total_seconds() // 60


def ensure_relative_time(work_day: WorkDay) -> WorkDay:
    if work_day.relative_to is not None:
        return work_day

    relative_date = _get_day_start(work_day.tasks[0].time)

    return WorkDay(
        tasks=work_day.tasks,
        staff_members=work_day.staff_members,
        relative_to=relative_date,
    )


def get_task_start_time_vector(
    work_day: WorkDay,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            task.time,
            relative_date=work_day.relative_to,
        )
        for task in work_day.tasks
    ]


def get_task_finish_time_vector(work_day: WorkDay) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            task.time, relative_date=work_day.relative_to
        )
        + task.duration
        for task in work_day.tasks
    ]


def get_worker_start_time_vector(
    work_day: WorkDay,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            staff_member.shift.start_time,
            relative_date=work_day.relative_to,
        )
        for staff_member in work_day.staff_members
    ]


def get_worker_finish_time_vector(
    work_day: WorkDay,
) -> list:
    return [
        _get_minutes_from_start_of_relative_date(
            staff_member.shift.finish_time,
            relative_date=work_day.relative_to,
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


def remove_tasks_with_no_time(workday: WorkDay) -> Tuple[WorkDay, List[InfeasibleTask]]:
    # This is a work around while we still have tasks with no time
    tasks_with_time = [task for task in workday.tasks if task.time != ""]
    infeasible_tasks = [
        InfeasibleTask(task=task, reason="No time set")
        for task in workday.tasks
        if task.time == ""
    ]

    return (
        WorkDay(
            tasks=tasks_with_time,
            staff_members=workday.staff_members,
            relative_to=workday.relative_to,
        ),
        infeasible_tasks,
    )


def sort_tasks_and_workers(workday: WorkDay) -> WorkDay:
    # This is a work around while we still have tasks with no time
    return WorkDay(
        tasks=sorted(workday.tasks, key=lambda task: task.time),
        staff_members=sorted(
            workday.staff_members,
            key=lambda staff_member: staff_member.shift.start_time,
        ),
        relative_to=workday.relative_to,
    )


def remove_infeasible_tasks(work_day: WorkDay) -> Tuple[WorkDay, List[InfeasibleTask]]:
    # This is a work around while we still have tasks with no time
    last_shift_finish = _get_minutes_from_start_of_relative_date(
        max(
            [staff_member.shift.finish_time for staff_member in work_day.staff_members]
        ),
        relative_date=work_day.relative_to,
    )
    first_shift_start = _get_minutes_from_start_of_relative_date(
        min([staff_member.shift.start_time for staff_member in work_day.staff_members]),
        relative_date=work_day.relative_to,
    )

    feasible_tasks = [
        task
        for task in work_day.tasks
        if _get_minutes_from_start_of_relative_date(
            task.time, relative_date=work_day.relative_to
        )
        >= first_shift_start
        and _get_minutes_from_start_of_relative_date(
            task.time, relative_date=work_day.relative_to
        )
        + task.duration
        <= last_shift_finish
    ]

    infeasible_tasks = [
        InfeasibleTask(
            task=task,
            reason="No staff available during this time",
        )
        for task in work_day.tasks
        if task not in feasible_tasks
    ]

    return (
        WorkDay(
            tasks=feasible_tasks,
            staff_members=work_day.staff_members,
            relative_to=work_day.relative_to,
        ),
        infeasible_tasks,
    )


def prepare_work_day(
    work_day: WorkDay,
    remove_unstaffed_tasks: bool = True,
) -> Tuple[WorkDay, List[InfeasibleTask]]:
    infeasible_tasks = []

    work_day, tasks_with_no_time = remove_tasks_with_no_time(work_day)
    infeasible_tasks.extend(tasks_with_no_time)

    work_day = sort_tasks_and_workers(work_day)
    work_day = ensure_relative_time(work_day)

    if not remove_unstaffed_tasks:
        work_day, unstaffed_tasks = remove_infeasible_tasks(work_day)
        infeasible_tasks.extend(unstaffed_tasks)

    _logger.warning(f"Removed {len(infeasible_tasks)} infeasible tasks")
    return work_day, infeasible_tasks
