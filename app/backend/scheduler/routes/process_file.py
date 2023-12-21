from fastapi import APIRouter, File, Form, UploadFile

from scheduler.models import (
    WorkDay,
    RosterProcessingResult,
    StudyScheduleProcessingResult,
)


router = APIRouter(
    prefix="/api/process-files",
    tags=["process-files"],
)


@router.post("/roster", response_model=RosterProcessingResult)
def process_roster(
    roster_file: UploadFile = File(...),
) -> RosterProcessingResult:
    # TODO(olivia): implement

    print(roster_file)
    return RosterProcessingResult(
        days=["1", "2", "3"],
    )


@router.post("/study-schedule", response_model=StudyScheduleProcessingResult)
def process_study_schedule(
    study_schedule_file: UploadFile = File(...),
) -> StudyScheduleProcessingResult:
    # TODO(olivia): implement

    print(study_schedule_file)
    return StudyScheduleProcessingResult(
        days=["1", "2", "3"],
        cohorts=["alpha", "beta", "gamma"],
    )


@router.post("/build-workday", response_model=WorkDay)
def build_workday(
    files: list[UploadFile] = File(...),
    json_data: str = Form(...),
) -> WorkDay:
    # TODO(olivia): implement

    print(files)
    print(json_data)
    return WorkDay(
        staff_members=[],
        tasks=[],
    )
