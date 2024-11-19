import json
import time

import requests
import os
from dotenv import load_dotenv
from datetime import timedelta, date

load_dotenv()
api_key = os.getenv('API_KEY')


def main():
    current_date = date.today()
    new_date = current_date
    while True:
        while new_date.weekday() > 4:
            new_date = new_date - timedelta(days=1)
        fetch_day(str(new_date))
        time.sleep(15)
        new_date = new_date - timedelta(days=1)


def fetch_day(day: str):
    request_link = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{day}?adjusted=true&include_otc=true&apiKey={api_key}"
    response = requests.get(request_link)
    print(f"Request link: {request_link}")
    print(f"code: {response.status_code}")
    with open(f"days/{day}.json", "w") as file:
        file.write(json.dumps(response.json(), separators=(',', ':'), indent=None, sort_keys=True))
    print(f"File saved to days/{day}.json")

if __name__ == '__main__':
    main()
