import sys
from fileprocess import *
from testcases import get_test_cases
from colorama import Fore

def test(file_name, problem):
    compile(file_name)

    test_cases = get_test_cases(f'https://open.kattis.com/problems/{problem}')

    if test_cases == None:
        return True

    print('Running Sample Test Cases:')

    passed_all = True
    failed_ctr = 0

    for index, test_case in enumerate(test_cases):
        print(f'Running sample test case #{index + 1} ...', end='', flush = True)
        
        output = execute(file_name, test_case['input']).strip()

        if output == test_case['output']:
            print(Fore.GREEN + f'\r✔ Sample test case #{index + 1} passed!', flush=True)
        else:
            failed_ctr += 1
            passed_all = False
            print(Fore.RED + f'\r✖ Sample test case #{index + 1} failed!', flush=True)
  

    if passed_all:
        print(Fore.GREEN + 'Result: Passed All Sample Test Cases!\n')
    else:
        print(Fore.RED + f'Result: Failed {failed_ctr} Test Cases :(\n')

    return passed_all
