
import logging
from pathlib import Path

from models import WorkDay
from solver.pipeline import run_solver
from solver.solve import InfeasibleException

_logger = logging.getLogger(__name__)


_ROOT_DIR = Path("scratch/solver/test_data")


# example 3 is infeasible

def generate_report(input_file: Path, output_dir: Path):

    # You can get your work day from anywhere, but here's an example loading from a file
    work_day = WorkDay.parse_file(input_file)

    _logger.info(f"Generating report for {input_file} in {output_dir}")

    try:
        run_solver(
            work_day=work_day,
            output_dir=output_dir,
            open_browser=True,
            solution_title=input_file.stem
        )
    except InfeasibleException as e:
        _logger.warning(f"Work day {input_file} is infeasible: {e}")


def main():
    for input in _ROOT_DIR.glob("*.json"):
        output_dir = _ROOT_DIR / input.stem
        output_dir.mkdir(exist_ok=True, parents=True)
        generate_report(input, output_dir)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
