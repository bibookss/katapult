import re
import sys
import requests
from utils import html_page


def parse_test_cases(raw_test_cases):
    test_cases = []
    raw_test_cases = list(map(str, raw_test_cases))

    for i in range(0, len(raw_test_cases), 2):
        input_text = re.search(r"<pre>(.*?)</pre>", raw_test_cases[i], re.DOTALL).group(1)
        output_text = re.search(r"<pre>(.*?)</pre>", raw_test_cases[i + 1], re.DOTALL).group(1)

        test_case = {
            'input' : input_text.strip(),
            'output' : output_text.strip()
        }

        test_cases.append(test_case)
    
    return test_cases



def get_test_cases(url):
    try:
        response = requests.get(url, data={'script' : 'true'})
        if response.status_code != 200:
            sys.exit('Error: problem does not exist!')
    except requests.exceptions.RequestException:
        sys.exit('An error occured getting test cases.')

    problem_page = html_page(response)
    table_elements = problem_page.select('table.sample')
    test_cases = []

    for table_element in table_elements:
        test_cases.extend(table_element.select('pre'))
 
    if len(test_cases) > 0:
        test_cases = parse_test_cases(test_cases)
    else:
        print('This problem does not provide sample test cases.')
        return None

    return test_cases

