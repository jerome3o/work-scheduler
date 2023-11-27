# runs solver on /solve endpoint
# statically serves the output directory

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models import Solution, WorkDay
from solver.pipeline import run_solver


app = FastAPI()


app.mount("/outputs", app=StaticFiles(directory="outputs"), name="outputs")


@app.get("/solve")
def solve(work_day: WorkDay) -> Solution:
    return run_solver(
        work_day=work_day,
        # todo: use a guid for each solution
        output_dir="outputs/example_report",
        open_browser=False,
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app=app)
