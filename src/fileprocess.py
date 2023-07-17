import os
import sys
import time
import subprocess


def compile(file_path): 
    curr_dir = os.getcwd()
    name, extension = os.path.basename(file_path).split('.')
    
    compile_commands = {
        'cpp': f'g++ {curr_dir}/{file_path} -o {curr_dir}/{name}',
        'java': f'javac {curr_dir}/{file_path}',
        'py': None
    }

    if extension in compile_commands:
        compile_command = compile_commands[extension]
        if compile_command is None:
            return
    else:
        sys.exit('Error: Invalid File Type!')

    try:
        subprocess.run(compile_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit('Compilation Error')



def execute(file_path, input_str):
    time.sleep(1)

    curr_dir = os.getcwd()
    path = os.path.dirname(file_path)
    name, extension = os.path.basename(file_path).split('.')

    run_commands = {
        'cpp': [f'{curr_dir}/{path}/{name}'],
        'java': ['java', '-cp', f'{curr_dir}/{path}', name],
        'py': ['python3', f'{curr_dir}/{file_path}']    
    }

    if extension in run_commands:
        run_command = run_commands[extension]
    else:
        sys.exit('Error: Invalid File Type!')

    process = subprocess.Popen(
        run_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8')

    stdout, stderr = process.communicate(input=input_str)
    
    if stderr:
        sys.exit(f'Error: {stderr}')
        
    return stdout

def parse_code(file_path, problem):
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