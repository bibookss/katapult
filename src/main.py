from auth import auth
from dotenv import dotenv_values
from upload import upload_file, get_submission_status, display_submission_status
import sys

if __name__ == "__main__":    
    config = dotenv_values('.env')
    username = config['USERNAME']
    password = config['PASSWORD']

    try:
        user = auth(username, password)

        if len(sys.argv) < 3:
            print('Usage: python main.py <file_path> <problem>')

        submission_id = upload_file(sys.argv[1], sys.argv[2], user)
        submission = get_submission_status(submission_id, user)
        display_submission_status(submission)

    except Exception as e:
        print(e)
        

    