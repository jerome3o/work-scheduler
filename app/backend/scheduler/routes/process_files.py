from fastapi import APIRouter, File, Form, UploadFile

from scheduler.models import (
    WorkDay,
    RosterProcessingResult,
    StudyScheduleProcessingResult,
    GenerateWorkDayOptions,
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

    return RosterProcessingResult(
        days=["1", "2", "from server"],
    )


@router.post("/study-schedule", response_model=StudyScheduleProcessingResult)
def process_study_schedule(
    study_schedule_file: UploadFile = File(...),
) -> StudyScheduleProcessingResult:
    # TODO(olivia): implement

    return StudyScheduleProcessingResult(
        days=["1", "2", "from server"],
        cohorts=["alpha", "beta", "from server"],
    )


@router.post("/build-workday", response_model=WorkDay)
def build_workday(
    study_schedule_files: list[UploadFile] = File(...),
    roster_file: UploadFile = File(...),
    additional_data: str = Form(...),
) -> WorkDay:
    options = GenerateWorkDayOptions.model_validate_json(additional_data)

    # TODO(olivia): implement

    print(study_schedule_files)
    print(roster_file)
    print(options)
    return WorkDay(
        staff_members=[],
        tasks=[],
    )
