from dataclasses import dataclass
from typing import List


@dataclass
class ModelParameters:
    task_start_vector: List[int]
    task_finish_vector: List[int]
    task_skillset_matrix: List[int]
    worker_start_vector: List[int]
    worker_finish_vector: List[int]
    worker_skillset_matrix: List[int]
