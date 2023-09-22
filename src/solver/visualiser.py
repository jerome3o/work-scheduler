from models import WorkDay
from solver.helpers import build_matrices, remove_tasks_with_no_time, load_work_day
from solver.models import ModelParameters


def visualise_model_parameters(model_parameters: ModelParameters):
    pass


def main():
    # todo define relative day somewhere in the workday

    data_files = [
        "test_data/solver/workday_example_1.json",
        "test_data/solver/workday_example_2.json",
        "test_data/solver/workday_example_3.json",
    ]

    for data_file in data_files:
        work_day = load_work_day(data_file)
        work_day = remove_tasks_with_no_time(work_day)
        model_parameters = build_matrices(work_day)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
