import requests
import json
from pytz import timezone
from datetime import datetime, time

def load_attempts(url,pages=1):
    for page in range(pages):
        params = {'page' : pages}
        response = requests.get(url,params)
        if response.status_code==200:
            users = json.loads(response.text)
            for user_info in users['records']:
                yield {
                    'username': user_info['username'],
                    'timestamp': user_info['timestamp'],
                    'timezone': user_info['timezone'],
                }

def get_midnighters(attempts):
    time_midnight = time(0,0,0)
    time_morning = time(6,0,0)
    midnightes = set()
    for attempt in attempts:
        if not attempt['timestamp'] is None:
            utc_time = datetime.fromtimestamp(attempt['timestamp'],tz=timezone(attempt['timezone'])).time()
            if time_midnight < utc_time < time_morning:
                midnightes.add(attempt['username'])
    return midnightes

def print_midnighters(midnighters):
    print('Список полуночников : ')
    count = 1
    for midnighter in list(midnighters):
        print('{}. {}'.format(count,midnighter))
        count += 1

if __name__ == '__main__':
    url = 'https://devman.org/api/challenges/solution_attempts/'
    attempts = load_attempts(url)
    print_midnighters(get_midnighters(attempts))