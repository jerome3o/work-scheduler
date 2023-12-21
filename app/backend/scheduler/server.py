from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from scheduler.constants import OUTPUT_ENDPOINT_ROOT, OUTPUT_FILE_ROOT
from scheduler.routes.process_file import router as process_file_router
from scheduler.routes.solve import router as solve_router


app = FastAPI()

app.include_router(process_file_router)
app.include_router(solve_router)

app.mount(
    OUTPUT_ENDPOINT_ROOT,
    app=StaticFiles(directory=OUTPUT_FILE_ROOT),
    name="outputs",
)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app="scheduler.server:app", reload=True)
