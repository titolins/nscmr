import os
from uuid import UUID

TESTING = True
MONGODB_DB = 'nscmr_test'

basedir = '/home/snil/dev/nscmr'

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'instance/uploads')
#UPLOADS_IMAGES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'img/')

DEBUG = True
MONGODB_DB = 'nscmr_test'

# sandbox
MUNDIPAGG_KEY = UUID('7075fc55-70ed-41f2-9def-95e5053f11dd')
MUNDIPAGG_ENDPOINT = 'https://sandbox.mundipaggone.com/'
