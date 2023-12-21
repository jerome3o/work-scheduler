from fastapi import APIRouter

from scheduler.models import WorkDay


router = APIRouter(
    prefix="/api/process-files",
    tags=["process-files"],
)


@router.post("/roster")
def process_roster():
    pass


@router.post("/study-schedule")
def process_study_schedule():
    pass


@router.post("/build-workday", response_model=WorkDay)
def build_workday() -> WorkDay:
    pass
