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
MUNDIPAGG_KEY = UUID('7075fc55-70ed-41f2-9def-95e5053f11dd')
MUNDIPAGG_ENDPOINT = 'https://sandbox.mundipaggone.com/'

GOOGLE_CLIENT_ID = "883320219445-ejvh51karin9m6dg9mbql56vjn0vp2ls.apps.googleusercontent.com"
