import json
from datetime import timedelta
from typing import List

from models import SolverOutput, TaskAllocation
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def _get_allocations_df(
    task_allocations: List[TaskAllocation],
    include_shift: bool = False,
) -> pd.DataFrame:
    data = []

    for task_allocation in task_allocations:
        if include_shift:
            data.append(
                {
                    "task_start": task_allocation.staff_member.shift.start_time,
                    "task_end": task_allocation.staff_member.shift.finish_time,
                    "staff_member": task_allocation.staff_member.name,
                    "label": task_allocation.staff_member.name + " Shift",
                }
            )

        for task in task_allocation.task:
            task_dict = json.loads(task.json())
            task_dict["staff_member"] = task_allocation.staff_member.name
            task_dict["label"] = task_allocation.staff_member.name
            task_dict["task_start"] = task.time
            task_dict["task_end"] = task.time + timedelta(minutes=task.duration)
            data.append(task_dict)

    return pd.DataFrame(data)


def visualise_shifts(task_allocations: List[TaskAllocation]) -> go.Figure:
    df = _get_allocations_df(task_allocations, include_shift=True)

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
    return fig


def visualise_workloads(allocations: List[TaskAllocation]) -> go.Figure:
    df = _get_allocations_df(allocations)
    fig = px.bar(
        df,
        x="staff_member",
        y="duration",
        color="title",
        hover_data=[
            "title",
            "study",
            "patient",
            "duration",
            "task_start",
            "required_attributes",
        ],
        barmode="stack",
    )
    fig.update_layout(showlegend=False)
    return fig


def main():
    f = "test_data/solver/workday_example_1.out.json"
    s = SolverOutput.parse_file(f)
    fig = visualise_shifts(s.allocations)
    fig.show()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
