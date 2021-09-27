# Development Server

from flask import Flask, request, jsonify
import os, json, uuid, subprocess

app = Flask(__name__)

@app.route('/')
def root():
    return 'GitHub Development Server is Running'

# ====================================================================================================================

@app.route('/deploy', methods=['POST'])
def deploy():
    json_data = request.get_json()
    # Verify keys
    if not json_data.get('repo'):
        return jsonify(status='error', message='Repo was not defined')
    if not json_data.get('run_command'):
        return jsonify(status='error', message='No run command was defined')  
    
    # Create config block for App
    block = {
        'appID': str(uuid.uuid4()),
        'repo': json_data.get('repo'),
        'branch': json_data.get('branch'),
        'run_command': json_data.get('run_command'),
        # 'firstbuild': 'default'
    }

    # Verify directory existence
    if not os.path.exists('./pipeline.json'):
        with open('pipeline.json', 'w') as file:
            json.dump({'Apps': []}, file)

    # Load new configuration
    with open('pipeline.json', 'r+') as file:
        pipeline = json.load(file)
        # Prevent Duplicates
        dup = False
        for app in pipeline['Apps']:
            if block.get('repo') == app.get('repo'):
                # Will work on updating values in the future
                dup = True
                message = 'Repo has already been piped!'
                break
        if not dup:
            pipeline['Apps'].append(block)
            file.seek(0)
            json.dump(pipeline, file, indent=2)
            message = 'Done.'
    return jsonify(status='success', message=message)

# ====================================================================================================================

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    # with open('hook.json', 'w') as file:
    #     json.dump(json_data, file, indent=4)
    with open('pipeline.json', 'r') as file:
        pipeline = json.load(file)
    for app in pipeline['Apps']:
        if app.get('repo') == json_data.get('repository').get('clone_url'):
            run_command = app.get('run_command')

    run_build(json_data, run_command)
    return jsonify(status='success')

def generate_build_scripts(build_path, repo, run_command, type) -> list:

    # Problem with accessing github when git command is used in 
    # conjuctgion with other command in a string block the bash scripts

    # Workaround that seems to work: 
    # Break script string into smaller blocks with git command as single lines

    if type == 'initial':
        block1 = \
f'git clone {repo} ./{build_path}'

        block3 = \
f'''cd "{build_path}"
{run_command}
echo "******************************************"'''

        block2 = \
f'''cd "{build_path}"
nohup {run_command} > app-dev.log 2>&1 &
echo $! > pid.txt'''
        return list([block1,block2])
  
    elif type == 'rebuild':
        block1 = \
f'''cd "{build_path}"
kill -9 `cat pid.txt`
rm pid.txt'''

        block2 = \
f'git -C ./{build_path} pull --rebase'

        block3 = \
f'''cd "{build_path}"
nohup {run_command} > app-dev.log 2>&1 &
echo $! > pid.txt'''

        sample = \
f'''#!/bin/bash
cd "{build_path}"
kill -9 `cat pid.txt`
rm pid.txt
git pull --rebase
nohup {run_command} > app-dev.log 2>&1 &
echo $! > pid.txt'''
        return list([block1,block2,block3])

def run_build(data, run_command):
    repo_object = data.get('repository')
    path = './' + repo_object.get('full_name')
    repo = repo_object.get('clone_url')
    run_command = run_command

    # Rebuild
    if os.path.exists(path):
        bash_scripts = generate_build_scripts(path, repo, run_command, 'rebuild')
        for script in bash_scripts:
            retries = 3
            # Handle error on git commands
            if script.startswith('git'):
                while retries > 0: 
                    try:
                        subprocess.check_call(script, shell=True)
                        break
                    except:
                        retries -= 1
            # Handle error to kill former process that as stopped running,
            # will work on smoother continuous integration in the future 
            elif '\nkill' in script:
                # print('yesssssssssss')
                try:
                    subprocess.check_call(script, shell=True)
                except:
                    pass
            else:            
                subprocess.check_call(script, shell=True)

    # Initial Build   
    if not os.path.exists(path):
        os.makedirs(path)
        bash_scripts = generate_build_scripts(path, repo, run_command, 'initial')
        for script in bash_scripts:
            retries = 3
            # Handle error on git commands
            if script.startswith('git'):
                while retries > 0: 
                    try:
                        process = subprocess.check_call(script, shell=True)
                        break
                    except:
                        retries -= 1
            else:            
                process = subprocess.check_call(script, shell=True)
            print(f'Code: {process}')

# ====================================================================================================================

@app.route('/test')
def test():
    path = './Tolu1/deployment-pipeline'
    repo = 'https://github.com/Tolu1/deployment-pipeline.git'
    run_command ='python3 test.py'
    
    # Rebuild
    if os.path.exists(path):
        bash_scripts = generate_build_scripts(path, repo, run_command, 'rebuild')
        for script in bash_scripts:
            retries = 3
            # Handle error on git commands
            if script.startswith('git'):
                while retries > 0: 
                    try:
                        process = subprocess.Popen(script, shell=True)
                        break
                    except:
                        retries -= 1
            # Handle error to kill former process that as stopped running,
            # will work on smoother continuous integration in the future 
            elif '\nkill' in script:
                # print('yesssssssssss')
                try:
                    subprocess.check_call(script, shell=True)
                except:
                    pass
            else:            
                process = subprocess.check_call(script, shell=True)
            # print(f'Code: {process}')

    # Initial Build   
    if not os.path.exists(path):
        os.makedirs(path)
        bash_scripts = generate_build_scripts(path, repo, run_command, 'initial')
        for script in bash_scripts:
            retries = 3
            # Handle error on git commands
            if script.startswith('git'):
                while retries > 0: 
                    try:
                        process = subprocess.check_call(script, shell=True)
                        break
                    except:
                        retries -= 1
            else:            
                process = subprocess.check_call(script, shell=True)
            print(f'Code: {process}')
    
    return jsonify(status='success')

# ====================================================================================================================

@app.route('/ping')
def ping():
    return 'Ping was successful!'

# ====================================================================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

