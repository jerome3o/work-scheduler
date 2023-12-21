from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ModelParameters:
    task_start_vector: List[int]
    task_finish_vector: List[int]
    task_skillset_matrix: List[int]
    worker_start_vector: List[int]
    worker_finish_vector: List[int]
    worker_skillset_matrix: List[int]


    def get_time_range(self) -> Tuple[int, int]:
        latest_task_finish = max(self.task_finish_vector)
        earliest_task_start = min(self.task_start_vector)

        latest_worker_finish = max(self.worker_finish_vector)
        earliest_worker_start = min(self.worker_start_vector)

        earliest_minute = min(earliest_task_start, earliest_worker_start)
        latest_minute = max(latest_task_finish, latest_worker_finish)

        return (int(earliest_minute), int(latest_minute))
