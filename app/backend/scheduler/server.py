from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from scheduler.constants import OUTPUT_ENDPOINT_ROOT, OUTPUT_FILE_ROOT
from scheduler.routes.process_files import router as process_file_router
from scheduler.routes.solve import router as solve_router


app = FastAPI()

app.include_router(process_file_router)
app.include_router(solve_router)

Path(OUTPUT_FILE_ROOT).mkdir(parents=True, exist_ok=True)

app.mount(
    OUTPUT_ENDPOINT_ROOT,
    app=StaticFiles(directory=OUTPUT_FILE_ROOT),
    name="outputs",
)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    from uvicorn import run

    run(app="scheduler.server:app", reload=True, host="0.0.0.0", port=8001)
