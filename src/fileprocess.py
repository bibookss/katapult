import os
import sys
import time
import subprocess


def compile(file_path): 
    curr_dir = os.getcwd()
    name, extension = os.path.basename(file_path).split('.')
    compile_command = ''

    if extension == 'cpp':
        compile_command = f'g++ {curr_dir}/{file_path} -o {curr_dir}/{name}'
    elif extension == 'java':
        compile_command = f'javac {curr_dir}/{file_path}'
    elif extension == 'py':
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
    run_command = []

    
    if extension == 'cpp':
        run_command = [f'{curr_dir}/{path}/{name}']
    elif extension == 'java':
        run_command = ['java', '-cp', f'{curr_dir}/{path}', name]
    elif extension == 'py':
        run_command = ['python3', f'{curr_dir}/{file_path}']
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
