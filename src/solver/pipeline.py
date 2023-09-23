from typing import Union
from pathlib import Path
from webbrowser import open as _open_browser

from models import WorkDay

from solver.solve import solve
from solver.report.generate import generate_report


def run_solver(
    work_day: WorkDay,
    output_dir: Union[str, Path],
    open_browser: bool = True,
):
    solution = solve(work_day)
    generate_report(solution, output_dir)

    if open_browser:
        _open_browser(str(Path(output_dir) / "index.html"))

    return solution

def main():
    # you don't need to load from a file, you can just pass in the WorkDay object
    input_file = "test_data/solver/workday_example_1.json"
    run_solver(
        work_day=WorkDay.parse_file(input_file),
        output_dir="outputs/example_report",
    )

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
