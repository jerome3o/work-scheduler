from src.models import WorkDay


def get_task_start_time_vector(work_day: WorkDay) -> list:
    # TODO(j.swannack): implement
    pass


def get_task_duration_vector(work_day: WorkDay) -> list:
    # TODO(j.swannack): implement
    pass


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
