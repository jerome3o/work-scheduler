import matplotlib.pyplot as plt

from models import WorkDay
from solver.helpers import build_matrices, prepare_work_day, load_work_day
from solver.model_parameters import ModelParameters


def visualise_model_parameters(model_parameters: ModelParameters):
    fig, ax = plt.subplots()

    n_tasks = len(model_parameters.task_start_vector)
    n_workers = len(model_parameters.worker_start_vector)

    for i in range(n_tasks):
        ax.plot(
            [
                model_parameters.task_start_vector[i],
                model_parameters.task_finish_vector[i],
            ],
            [i, i],
            color="blue",
        )

    for i in range(n_workers):
        y = i + n_tasks
        ax.plot(
            [
                model_parameters.worker_start_vector[i],
                model_parameters.worker_finish_vector[i],
            ],
            [y, y],
            color="red",
        )

    plt.show()

def main():
    # todo define relative day somewhere in the workday
    import matplotlib
    matplotlib.use("tkAgg")

    data_files = [
        "test_data/solver/workday_example_1.json",
        "test_data/solver/workday_example_2.json",
        "test_data/solver/workday_example_3.json",
    ]

    for data_file in data_files:
        work_day = load_work_day(data_file)
        work_day, _ = prepare_work_day(work_day)
        model_parameters = build_matrices(work_day)
        visualise_model_parameters(model_parameters)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
