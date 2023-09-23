import json
from datetime import timedelta
from typing import List

from models import SolverOutput, TaskAllocation, Task, StaffMember
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def visualise_task_allocations(task_allocations: List[TaskAllocation]):

    data = []

    for task_allocation in task_allocations:

        data.append(
            {
                "task_start": task_allocation.staff_member.shift.start_time,
                "task_end": task_allocation.staff_member.shift.finish_time,
                "staff_member": task_allocation.staff_member.name,
                "label": task_allocation.staff_member.name + " Shift"
            }
        )

        for task in task_allocation.task:
            task_dict = json.loads(task.json())
            task_dict["staff_member"] = task_allocation.staff_member.name
            task_dict["label"] = task_allocation.staff_member.name
            task_dict["task_start"] = task.time
            task_dict["task_end"] = task.time + timedelta(minutes=task.duration)
            data.append(task_dict)

    df = pd.DataFrame(data)

    # Convert time columns to datetime format
    df["task_start"] = pd.to_datetime(df["task_start"])
    df["task_end"] = pd.to_datetime(df["task_end"])

    # Create gantt chart
    fig = px.timeline(
        df,
        x_start="task_start",
        x_end="task_end",
        y="label",
        color="staff_member",
        hover_data=df.columns,
    )
    fig.update_yaxes(
        autorange="reversed"
    )  # reverse the order of tasks, it's more natural in gantt charts

    fig.show()


def visualise_solution(solution: SolverOutput):
    visualise_task_allocations(solution.allocations)


def main():
    f = "test_data/solver/workday_example_1.out.json"
    s = SolverOutput.parse_file(f)
    visualise_solution(s)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
