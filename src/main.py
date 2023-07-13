from auth import auth
from test import test
from dotenv import dotenv_values
from colorama import Fore
from upload import upload_file, get_submission_status, display_submission_status
import argparse
import sys

if __name__ == "__main__":    
    config = dotenv_values('.env')
    username = config['USERNAME']
    password = config['PASSWORD']
    
    parser = argparse.ArgumentParser(description='Python script to automatically test and submit your code to Kattis.')
    
    parser.add_argument('-t', action='store_true', help='Test code with all the sample test cases.')
    parser.add_argument('-s', action='store_true', help='Submit code to Kattis.')
    parser.add_argument('-ts', action='store_true', help='Test and submit the program.')

    parser.add_argument('program', help='Program file to submit')
    parser.add_argument('problem', help='Problem name')

    args = parser.parse_args()

    program_file = args.program
    problem_name = args.problem

    try:
        user = auth(username, password)
        
        if args.t:
            test_case_res = test(program_file, problem_name)

        if args.s:
            submission_id = upload_file(program_file, problem_name, user)
            submission = get_submission_status(submission_id, user)
            display_submission_status(submission)

        if args.ts:
            test_case_res = test(program_file, problem_name)
            
            if test_case_res == True:
                submission_id = upload_file(program_file, problem_name, user)
                submission = get_submission_status(submission_id, user)
                display_submission_status(submission)
            else:
                print(Fore.RESET + '\nSome sample test cases failed. Code will not be submitted.')

        if not args.t and not args.s and not args.ts:
            sys.exit('Usage: katapult [-t] [-s] [-ts] <path/to/file> <problem_name>')
            

    except Exception as e:
        print(e)
        

    
