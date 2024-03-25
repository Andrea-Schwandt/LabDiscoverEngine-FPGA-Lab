#!/usr/bin/env bash

# Import the virtual environment
source /home/vrlab/tmp/lde-installation/lde-env/bin/activate

# Change directory to the deployment directory
cd /home/vrlab/tmp/lde-installation/hbrs

# Setting variables before prodrc so you can override them there
export SCRIPT_NAME=/lde
export SESSION_COOKIE_PATH=/lde
export PORT=8080
export BIND=0.0.0.0
export KEEP_ALIVE=75
export WORKERS=9

# Import prodrc configuration (if it exists)
if [ -f prodrc ]; then
    source prodrc
fi

# Locate scripts/wsgi_app.py
export PYTHONPATH=$PYTHONPATH:scripts

# Run gunicorn
exec gunicorn --workers $WORKERS --keep-alive $KEEP_ALIVE --bind $BIND:$PORT wsgi_app:application
