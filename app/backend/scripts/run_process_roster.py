# import TestClient from fastapi.testclient

from fastapi.testclient import TestClient

from scheduler.server import app

_ROSTER_FILE = "scratch/test_data/example_roster.xlsx"


def main():
    client = TestClient(app)
    response = client.post(
        "/api/process-files/roster",
        files={"roster_file": open(_ROSTER_FILE, "rb")},
    )
    print(response.json())


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
