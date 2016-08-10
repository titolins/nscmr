import os, sys

# change this to indicate the correct configuration
os.environ['APP_CONFIG_FILE'] = '/var/www/nscmr/nscmr/config/testing.py'
sys.path.insert (0,'/var/www/nscmr')
os.chdir("/var/www/nscmr")

from nscmr import app as application
