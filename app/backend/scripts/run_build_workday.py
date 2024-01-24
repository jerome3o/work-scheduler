# import TestClient from fastapi.testclient
import json

from fastapi.testclient import TestClient

from scheduler.server import app


_ROSTER_FILE = "scratch/test_data/example_roster.xlsx"
_STUDY_SCHEDULE_FILE = [
    "scratch/test_data/example_study_schedule_1.xlsx",
    "scratch/test_data/example_study_schedule_2.xlsx",
]


def main():
    client = TestClient(app)

    # study_schedule_files: list[UploadFile] = File(...),
    # roster_file: UploadFile = File(...),
    # additional_data: str = Form(...),

    response = client.post(
        "/api/process-files/build-workday",
        files=[
        ("study_schedule_files", ("Arctic Schedule of Assessments.xlsx", open(_STUDY_SCHEDULE_FILE[0], "rb"))),
        ("study_schedule_files", ("Glow Schedule of Assessments.xlsx", open(_STUDY_SCHEDULE_FILE[1], "rb"))),
        ("roster_file", ("example_roster.xlsx", open(_ROSTER_FILE, "rb"))),
        ],
        # GenerateWorkDayOptions
        data={
            "additional_data": json.dumps(
                {
                    "studyScheduleOptions": [
                        {"day": "1", "cohort": "2", "patients": 2},
                        {"day": "1", "cohort": "4", "patients": 4},
                    ],
                    "rosterDay": "MON 07 AUG",
                }
            ),
        },
    )
    print(response.json())


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
