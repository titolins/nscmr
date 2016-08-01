import os
from uuid import UUID

basedir = '/var/www/nscmr'

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'instance/uploads')
#UPLOADS_IMAGES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'img/')

DEBUG = False
TESTING = True

SUPPORT_CONTACT = 'contato@studioduvet.com.br'
MONGODB_DB = 'nscmr_test'

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = MONGODB_DB

# sandbox
MUNDIPAGG_KEY = UUID('7075fc55-70ed-41f2-9def-95e5053f11dd')
MUNDIPAGG_ENDPOINT = 'https://sandbox.mundipaggone.com/'

GOOGLE_CLIENT_ID = "883320219445-ejvh51karin9m6dg9mbql56vjn0vp2ls.apps.googleusercontent.com"

# server test app settings (change for production)
FB_APP_ID = "1053748188074292"
FB_APP_SECRET = "654c8683322a23800b4645b5ede3c832"
FB_APP_SCOPE = "public_profile,email"
