import matplotlib.pyplot as plt

from models import WorkDay
from solver.helpers import build_matrices, prepare_work_day, load_work_day
from solver.model_parameters import ModelParameters


def build_worker_task_count_plot(
    model_parameters: ModelParameters,
    ax: plt.Axes = None,
    title: str = "Model Parameters",
):
    if ax is None:
        _, ax = plt.subplots()

    latest_task_finish = max(model_parameters.task_finish_vector)
    earliest_task_start = min(model_parameters.task_start_vector)

    latest_worker_finish = max(model_parameters.worker_finish_vector)
    earliest_worker_start = min(model_parameters.worker_start_vector)

    earliest_minute = min(earliest_task_start, earliest_worker_start)
    latest_minute = max(latest_task_finish, latest_worker_finish)

    x = range(int(earliest_minute), int(latest_minute))

    task_count = [
        sum(
            [
                1
                for task_start, task_finish in zip(
                    model_parameters.task_start_vector,
                    model_parameters.task_finish_vector,
                )
                if task_start <= minute <= task_finish
            ]
        )
        for minute in x
    ]

    worker_count = [
        sum(
            [
                1
                for worker_start, worker_finish in zip(
                    model_parameters.worker_start_vector,
                    model_parameters.worker_finish_vector,
                )
                if worker_start <= minute <= worker_finish
            ]
        )
        for minute in x
    ]

    ax.plot(x, task_count, label="Tasks")
    ax.plot(x, worker_count, label="Workers")

    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel("Time (minutes)")
    ax.legend()

    return ax


def build_parameter_plot(
    model_parameters: ModelParameters,
    ax: plt.Axes = None,
    title: str = "Model Parameters",
):
    if ax is None:
        _, ax = plt.subplots()

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

    ax.set_title(title)
    ax.set_ylabel("Task / Worker")
    ax.set_xlabel("Time (minutes)")

    # Legend that accounts for colours
    ax.plot([], [], color="blue", label="Task")
    ax.plot([], [], color="red", label="Worker")
    ax.legend()

    return ax

def visualise_model_parameters(
    model_parameters_feasible: ModelParameters,
    model_parameters_infeasible: ModelParameters,
):
    fig, ((f_ax, if_ax), (f_wt_ax, if_wt_ax)) = plt.subplots(2, 2)

    build_parameter_plot(model_parameters_feasible, ax=f_ax, title="Feasible Tasks Only")
    build_parameter_plot(model_parameters_infeasible, ax=if_ax, title="Infeasible Tasks Included")

    build_worker_task_count_plot(model_parameters_feasible, ax=f_wt_ax, title="Feasible Tasks Only")
    build_worker_task_count_plot(model_parameters_infeasible, ax=if_wt_ax, title="Infeasible Tasks Included")

    f_ax.set_xlim(
        if_ax.get_xlim()
    )
    f_wt_ax.set_xlim(
        if_wt_ax.get_xlim()
    )

    fig.tight_layout()

    plt.show()
    print("hey")


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
        work_day_feasible, _ = prepare_work_day(work_day)
        work_day_infeasible, _ = prepare_work_day(work_day, remove_unstaffed_tasks=False)
        model_parameters_feasible = build_matrices(work_day_feasible)
        model_parameters_infeasible = build_matrices(work_day_infeasible)
        visualise_model_parameters(
            model_parameters_feasible,
            model_parameters_infeasible,
        )

        break


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
