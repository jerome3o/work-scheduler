# import TestClient from fastapi.testclient

from fastapi.testclient import TestClient

from scheduler.server import app

_STUDY_SCHEDULE_FILE = "scratch/test_data/example_study_schedule_1.xlsx"


def main():
    client = TestClient(app)
    response = client.post(
        "/api/process-files/study-schedule",
        files={"study_schedule_file": open(_STUDY_SCHEDULE_FILE, "rb")},
    )
    print(response.json())


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
