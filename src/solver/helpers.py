from datetime import datetime

from src.models import WorkDay


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


def get_task_duration_vector(work_day: WorkDay) -> list:
    return [
        task.duration
        for task in work_day.tasks
    ]


def get_worker_start_time_vector(work_day: WorkDay) -> list:
    # TODO(j.swannack): implement
    pass


def get_worker_end_time_vector(work_day: WorkDay) -> list:
    # TODO(j.swannack): implement
    pass


def get_worker_skillset_matrix(work_day: WorkDay) -> list:
    # TODO(j.swannack): implement
    # This will be a one-hot encoding of the worker's skillset
    # With rows/cols being workers/skills
    pass


def get_task_skillset_matrix(work_day: WorkDay) -> list:
    # This will be a one-hot encoding of the task's required skillset
    # With rows/cols being tasks/skills
    pass
