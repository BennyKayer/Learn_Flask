# Virtual Envs
## Create
py -3 -m venv venv
## Activate - must be in cmd
venv\Scripts\activate
# Flask's Env
## Running Server
set FLASK_APP=server.py
flask run
## Enabling Debugger
set FLASK_ENV=development