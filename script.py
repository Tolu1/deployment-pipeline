# One-time script to initiate pipeline
from github_deploy import createPipeline

# =========
# Run Once
# =========

                                                            # =========
                                                            # Example
                                                            # =========

# Update to your own values.
REPO = 'https://github.com/Tolu1/deployment-pipeline.git'
BRANCH = 'main'
DEV_SERVER_HOSTNAME = 'https://a10a-105-112-72-191.ngrok.io'
RUN_COMMAND = 'python3 test.py' # will run test.py once code is pushed.

pipe = createPipeline(repo=REPO, branch=BRANCH)
print('Installing pipeline...')
status, message = pipe.install(RUN_COMMAND, f'{DEV_SERVER_HOSTNAME}/deploy')
if status == 'success':
    print(f'{message}')
    print(f"You must add hook '{DEV_SERVER_HOSTNAME}/webhook' \non your GitHub repo to trigger automatic rebuild")
else:
    print('Pipeline could not be installed!')
    print(f'--> {message}')