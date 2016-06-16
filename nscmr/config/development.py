import os
from uuid import UUID

basedir = '/home/snil/dev/nscmr'

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'instance/uploads')
#UPLOADS_IMAGES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'img/')

DEBUG = True
MONGODB_DB = 'nscmr_dev'

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = MONGODB_DB

# sandbox
MUNDIPAGG_KEY = UUID('87328324-8DA6-459E-9948-5431F5A183FA')
MUNDIPAGG_ENDPOINT = 'https://sandbox.mundipaggone.com/'


