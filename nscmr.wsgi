import os

os.environ['APP_CONFIG_FILE'] = '/var/www/nscmr/nscmr/config/development.py'

from nscmr import app as application
