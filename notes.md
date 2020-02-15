# Virtual Envs
## Create
py -3 -m venv venv
## Activate 
venv\Scripts\activate <- for cmd
source venv/Scripts/activate <- for git bash
# Flask's Env
## Running Server
set FLASK_APP=server.py
flask run
## Enabling Debugger
set FLASK_ENV=development