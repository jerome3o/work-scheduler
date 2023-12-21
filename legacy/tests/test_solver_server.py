# This is an integration test that is to be run manually with a local server running
# TODO: Turn into proper test
import requests
import json

import webbrowser

from models import WorkDay

_SERVER_URL = "http://localhost:8000"


def main():

    with open("scratch/solver/test_data/workday_example_1.json") as json_file:
        work_day = WorkDay.model_validate_json(json_file.read())
        data = json.loads(work_day.model_dump_json())

    response = requests.post(
        f"{_SERVER_URL}/solve",
        json=data,
    )

    data = response.json()
    webbrowser.open(f'{_SERVER_URL}{data["report_location"]}')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
