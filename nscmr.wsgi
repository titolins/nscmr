import os

# change this to indicate the correct configuration
os.environ['APP_CONFIG_FILE'] = '/app/nscmr/config/testing.py'

from nscmr import app as application
