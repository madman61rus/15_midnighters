import requests
import json
from pytz import timezone
from datetime import datetime, time

TIME_MIDNIGHT = time(0,0,0)
TIME_MORNING = time(6,0,0)

def load_attempts(url):
    count_of_pages = requests.get(url).json()['number_of_pages']
    for page in range(1,count_of_pages+1):
        params = {'page' : page}
        response = requests.get(url,params)
        if response.status_code==200:
            users = json.loads(response.text)
            yield from users['records']

def is_user_midnighter(attempt):
    if not attempt['timestamp'] is None:
        utc_time = datetime.fromtimestamp(attempt['timestamp'], tz=timezone(attempt['timezone'])).time()
        if TIME_MIDNIGHT < utc_time < TIME_MORNING:
            return True
        else:
            return False

def get_midnighters(attempts):
    return {attempt['username'] for attempt in attempts if is_user_midnighter(attempt)}


def print_midnighters(midnighters):
    print('Список полуночников : ')
    for counter,midnighter in list(enumerate(midnighters)):
        print('{}. {}'.format(counter,midnighter))

if __name__ == '__main__':
    url = 'https://devman.org/api/challenges/solution_attempts/'
    attempts = load_attempts(url)
    print_midnighters(get_midnighters(attempts))