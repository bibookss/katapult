import requests 
import re
import os
import time
from colorama import Fore
from utils import html_page
from fileprocess import parse_code

def get_submission_id(response):
    pattern = r"Submission ID: (\d+)"
    match = re.search(pattern, response.text)
    submission_id = match.group(1)

    return submission_id

def submit(file_path, problem, user):
    print(Fore.RESET + 'Submitting Code ...', end='', flush=True)

    submit_url = f'https://open.kattis.com/problems/{problem}/submit'
    payload = parse_code(file_path, problem)
    response = requests.post(submit_url, json=payload, cookies=user.cookie)

    if not response:
        raise Exception('Problem not found!')

    return get_submission_id(response)
    

def get_submission_status(submission_id, user):
    time.sleep(5)

    url = f'https://open.kattis.com/submissions/{submission_id}'
    response = requests.get(url, cookies=user.cookie)

    submission_page = html_page(response)
    table = submission_page.find('tbody')
    submission = table.select('tr[data-submission-id]')

    ttime = submission[0].find('td', {'data-type': 'time'}).text.strip()
    status = submission[0].find('td', {'data-type': 'status'}).text.strip()
    lang = submission[0].find('td', {'data-type': 'lang'}).text.strip()
    cpu = submission[0].find('td', {'data-type': 'cpu'}).text.strip()
    testcases = submission[0].find('td', {'data-type': 'testcases'}).text.strip()

    return {
        'id': submission_id,
        'time': ttime,
        'status': status,
        'lang': lang,
        'cpu': cpu,
        'testcases': testcases
    }

def display_submission_status(submission_status):
    print('\rSubmission Status:', flush=True)
    print("ID:".ljust(15), end=" ")
    print(submission_status["id"])
    print("Time:".ljust(15), end=" ")
    print(submission_status["time"])

    status = submission_status["status"]
    print("Status:".ljust(15), end=" ")
    if status == "Accepted":
        print(f'{Fore.GREEN}{status}{Fore.RESET}')
    else:
        print(f'{Fore.RED}{status}{Fore.RESET}')
    
    print("Language:".ljust(15), end=" ")
    print(submission_status["lang"])
    print("CPU:".ljust(15), end=" ")
    print(submission_status["cpu"])
    print("Test Cases:".ljust(15), end=" ")
    print(submission_status["testcases"])