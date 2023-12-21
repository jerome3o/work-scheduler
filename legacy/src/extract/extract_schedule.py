import os

from src.models import StudySchedule

_EXCEL_PATH = os.environ.get("EXCEL_PATH")
_READ_PASSWORD = os.environ.get("READ_PASSWORD")

def extract_from_schedule_workbook(
    workbook_path: str,
    day_of_interest: int,
    read_password: str,
) -> StudySchedule:
    print("workbook_path: ", workbook_path)
    print("day_of_interest: ", day_of_interest)
    print("read_password: ", read_password)


def main():
    extract_from_schedule_workbook(
        workbook_path=_EXCEL_PATH,
        day_of_interest=5,
        read_password=_READ_PASSWORD
    )

if __name__ == "__main__":
    main()