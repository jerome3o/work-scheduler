from fastapi import FastAPI

from models import Solution, SolverOutput, SolverInput


app = FastAPI()


@app.get("/solve")
def solve(solver_input: SolverInput) -> SolverOutput:
    pass


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app=app)
