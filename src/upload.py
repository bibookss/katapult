import requests 
import re
import os
import time
from colorama import Fore
from utils import html_page

def process_file(file_path, problem):
    file_name = os.path.basename(file_path)
    language = file_name.split('.')[-1]

    language_map = {
        'py': 'Python 3',
        'cpp': 'C++',
        'java': 'Java',
        'c': 'C',
    }

    with open(file_path, 'r') as file:
        code = file.read()
        payload = {
            "files": [
                {
                    "filename": file_name,
                    "code": code,
                    "id": 0,
                    "session": None
                }
            ],
            "language": language_map[language],
            "mainclass": file_name,
            "problem": problem,
        }
    
    return payload

def get_submission_id(response):
    pattern = r"Submission ID: (\d+)"
    match = re.search(pattern, response.text)
    submission_id = match.group(1)

    return submission_id

def upload_file(file_path, problem, user):
    print(Fore.RESET + 'Submitting Code:')

    submit_url = f'https://open.kattis.com/problems/{problem}/submit'
    payload = process_file(file_path, problem)
    response = requests.post(submit_url, json=payload, cookies=user.cookie)

    if not response:
        raise Exception('Problem not found!')

    return get_submission_id(response)
    

def get_submission_status(submission_id, user):
    time.sleep(10)

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
        'time': ttime,
        'status': status,
        'lang': lang,
        'cpu': cpu,
        'testcases': testcases
    }

def display_submission_status(submission_status):
    print('Submission Status:')
    print(f'Time: {submission_status["time"]}')
    print(f'Status: {submission_status["status"]}')
    print(f'Language: {submission_status["lang"]}')
    print(f'CPU: {submission_status["cpu"]}')
    print(f'Test Cases: {submission_status["testcases"]}')
