# Basic Jinja2 template rendering

import json
from pathlib import Path
from typing import Union
import jinja2

from models import Solution
from solver.visualisation.solution import visualise_shifts, visualise_workloads

_REPORT_ROOT = Path() / "outputs" / "reports"
_STATIC_DIR = Path(__file__).parent / "static"

_SHIFTS_PLOT_FILENAME = "shifts.html"
_WORKLOAD_PLOT_FILENAME = "workloads.html"


def build_report(
    solution: Solution,
    report_output_dir: Union[str, Path],
):
    report_output_dir = Path(report_output_dir)
    report_output_dir.mkdir(parents=True, exist_ok=True)

    template_dir = Path(__file__).parent / "templates"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )

    context = build_context(solution, report_output_dir)

    template = env.get_template("report.html.j2")
    return template.render(**context)


def build_context(
    solution: Solution,
    report_output_dir: Union[str, Path],
):
    report_output_dir = Path(report_output_dir)
    report_output_dir.mkdir(parents=True, exist_ok=True)

    # Copy contents from static dir to report output dir
    for static_file in _STATIC_DIR.glob("*"):
        if static_file.is_file():
            (report_output_dir / static_file.name).write_text(static_file.read_text())

    # Visualise shifts
    shifts_fig = visualise_shifts(solution.output.allocations)
    shifts_fig.write_html(str(report_output_dir / _SHIFTS_PLOT_FILENAME))

    # Visualise workloads
    workloads_fig = visualise_workloads(solution.output.allocations)
    workloads_fig.write_html(str(report_output_dir / _WORKLOAD_PLOT_FILENAME))

    return {
        "solution": json.loads(solution.json()),
        "summary": {
            "time": solution.meta.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "n_staff": len(solution.output.allocations),
            "n_tasks": len(solution.input.processed_work_day.tasks),
        },
        "plots": {
            "shifts": _SHIFTS_PLOT_FILENAME,
            "workloads": _WORKLOAD_PLOT_FILENAME,
        }
    }


def main():
    solution = Solution.parse_file("test_data/solver/workday_example_1.out.json")
    report_dir = _REPORT_ROOT / solution.meta.solution_id
    text = build_report(solution, report_output_dir=report_dir)
    (report_dir / "index.html").write_text(text)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
