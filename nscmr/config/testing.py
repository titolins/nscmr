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

GOOGLE_CLIENT_ID = "883320219445-ejvh51karin9m6dg9mbql56vjn0vp2ls.apps.googleusercontent.com"

# dev (test app) settings (change for production)
FB_APP_ID = "1050879885027789"
FB_APP_SECRET = "826f7fca7e04f05e9d4bae3de5a8e7a2"
FB_APP_SCOPE = "public_profile,email"
