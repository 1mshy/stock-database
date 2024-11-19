import datetime
import json
import time

import requests
import os
from dotenv import load_dotenv
from datetime import timedelta, date
import logging

logger = logging.getLogger(__name__)
load_dotenv()
api_key = os.getenv('API_KEY')
days_path = './days'
logging_path = './logging'


def main():
    current_date = get_last_recorded_date()
    new_date = current_date
    while True:
        while new_date.weekday() > 4:
            new_date = new_date - timedelta(days=1)
        fetch_day(new_date.strftime("%Y-%m-%d"))
        time.sleep(15)
        new_date = new_date - timedelta(days=1)


def fetch_day(day: str):
    request_link = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{day}?adjusted=true&include_otc=true&apiKey={api_key}"
    response = requests.get(request_link)
    log(f"Request link: {request_link}")
    log(f"Finished with code: {response.status_code} - {response}")
    with open(f"{days_path}/{day}.json", "w") as file:
        file.write(json.dumps(response.json(), separators=(',', ':'), indent=None, sort_keys=True))
    log(f"Json data saved to {days_path}/{day}.json")


def create_folders():
    try:
        os.mkdir(days_path)
    except FileExistsError:
        log(f"Directory '{days_path}' already exists, continuing")

    try:
        os.mkdir(logging_path)
    except FileExistsError:
        log(f"Directory '{logging_path}' already exists, continuing")


def get_last_recorded_date() -> date:
    files = os.listdir(days_path)
    files.sort()
    if len(files) == 0:
        return date.today() - timedelta(days=1)
    last_date = files[0].split(".")[0]
    log(f"Will be starting at: {last_date}")
    return datetime.datetime.fromisoformat(last_date)


def setup_logging():
    logging.basicConfig(filename=f'{logging_path}/{date.today().strftime("%m-%d-%Y")}', level=logging.INFO)
    logger.info('Started')


def log(anything):
    logger.info(str(anything))
    print(anything)


if __name__ == '__main__':
    create_folders()
    setup_logging()
    main()
    logger.info('Finished')
