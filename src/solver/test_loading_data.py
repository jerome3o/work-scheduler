from models import WorkDay

_DATA_FILE = "test_data/solver/workday.json"


def main():
    work_day = WorkDay.parse_file(_DATA_FILE)
    print(work_day.json(indent=4))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
