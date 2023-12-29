from typing import Annotated
from openpyxl import load_workbook
from scheduler.constants import PASSWORD
import msoffcrypto
from fastapi import APIRouter, File, Form, UploadFile

from io import BytesIO

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
    roster_file: UploadFile = Annotated[bytes, File()],
) -> RosterProcessingResult:
    # TODO(olivia): implement

    encrypted = BytesIO(roster_file.file.read())
    decryped = BytesIO()
    file = msoffcrypto.OfficeFile(encrypted)

    # TODO: the password needs to be input
    file.load_key(password=PASSWORD)
    file.decrypt(decryped)

    wb = load_workbook(decryped)
    print(wb.sheetnames)

    return RosterProcessingResult(
        days=wb.sheetnames,
    )


@router.post("/study-schedule", response_model=StudyScheduleProcessingResult)
def process_study_schedule(
    study_schedule_file: UploadFile = File(...),
) -> StudyScheduleProcessingResult:
    # TODO(olivia): implement

    f = BytesIO(study_schedule_file.file.read())

    wb = load_workbook(f)
    print(wb.sheetnames)

    return StudyScheduleProcessingResult(
        days=wb.sheetnames,
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
