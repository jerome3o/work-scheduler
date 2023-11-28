# runs solver on /solve endpoint
# statically serves the output directory


from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models import Solution, WorkDay
from solver.pipeline import run_solver

_OUTPUT_FILE_ROOT = Path("outputs")
_OUTPUT_ENDPOINT_ROOT = "/outputs"


app = FastAPI()

app.mount(_OUTPUT_ENDPOINT_ROOT, app=StaticFiles(directory="outputs"), name="outputs")


@app.post("/solve")
def solve(work_day: WorkDay) -> Solution:

    # todo: use a guid for each solution
    output_dir = _OUTPUT_FILE_ROOT / "example"
    output_dir.mkdir(parents=True, exist_ok=True)

    solution = run_solver(
        work_day=work_day,
        output_dir=output_dir,
        open_browser=False,
    )

    solution.report_location = (
        Path(_OUTPUT_ENDPOINT_ROOT)
        / output_dir.relative_to(_OUTPUT_FILE_ROOT)
        / "index.html"
    )
    return solution


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app=app)
