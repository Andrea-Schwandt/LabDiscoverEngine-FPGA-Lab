import sys
sys.path.append('../..') # labdiscoverylib
import os
from c_x_lab import create_app

if os.environ.get('FLASK_DEBUG') == '1':
    config_name = 'development'
else:
    config_name = os.environ.get('FLASK_CONFIG') or 'default'

app = create_app(config_name)
