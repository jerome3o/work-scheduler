# runs solver on /solve endpoint
# statically serves the output directory


from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from scheduler.models import Solution, WorkDay
from scheduler.solver.pipeline import run_solver

_OUTPUT_FILE_ROOT = Path("outputs")
_OUTPUT_ENDPOINT_ROOT = "/outputs"
_FE_FILE_ROOT = "/"


_count = 0

app = FastAPI()

app.mount(_OUTPUT_ENDPOINT_ROOT, app=StaticFiles(directory="outputs"), name="outputs")


@app.get("/")
def root():
    # redirect to index.html
    return RedirectResponse(url="/index.html")


@app.get("/api/example_endpoint")
def example_endpoint():
    global _count

    _count = _count + 1
    return {"message": "nice" if _count % 2 == 0 else "not nice", "count": _count}


@app.post("/api/process-excel")
def process_excel():
    # TODO: file uploads
    #   * server side look for "fastapi file uploads"
    #   * frontend side look for "vanilla javascript file upload
    # I think "multipart upload" is a thing you're gonna wanna look at

    # TODO: once you have the excel files somewhere, run your processing code
    #   Maybe also call the solver?
    pass


@app.post("/api/solve")
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


app.mount(_FE_FILE_ROOT, app=StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app="server:app", reload=True)
