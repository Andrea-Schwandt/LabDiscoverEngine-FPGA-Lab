#!/usr/bin/env bash

# Import the virtual environment
source /home/vrlab/tmp/lde-installation/lde-env/bin/activate

# Change directory to the deployment directory
cd /home/vrlab/tmp/lde-installation/hbrs

# Setting variables before prodrc so you can override them there
export FLASK_CONFIG=production

# Import prodrc configuration (if it exists)
if [ -f prodrc ]; then
    source prodrc
fi

# Run the worker
exec lde worker run
