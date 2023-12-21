from pathlib import Path

from fastapi import APIRouter

from scheduler.constants import OUTPUT_ENDPOINT_ROOT, OUTPUT_FILE_ROOT
from scheduler.models import Solution, WorkDay
from scheduler.solver.pipeline import run_solver


router = APIRouter(
    prefix="/api/solve",
    tags=["solve"],
)


@router.post("/")
def solve(work_day: WorkDay) -> Solution:
    # todo: use a guid for each solution
    output_dir = OUTPUT_FILE_ROOT / "example"
    output_dir.mkdir(parents=True, exist_ok=True)

    solution = run_solver(
        work_day=work_day,
        output_dir=output_dir,
        open_browser=False,
    )

    solution.report_location = (
        Path(OUTPUT_ENDPOINT_ROOT)
        / output_dir.relative_to(OUTPUT_FILE_ROOT)
        / "index.html"
    )
    return solution
