import os
from uuid import UUID

basedir = '/var/www/nscmr'

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'instance/uploads')
#UPLOADS_IMAGES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'img/')

DEBUG = False
TESTING = False

SUPPORT_CONTACT = 'contato@studioduvet.com.br'
MONGODB_DB = 'nscmr'

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = MONGODB_DB

PAGSEGURO_TOKEN = "3D4DEFEA09EA4B4B9887D15EA19915CA"
PAGSEGURO_ENDPOINT = "https://ws.pagseguro.uol.com.br/v2/checkout/"

GOOGLE_CLIENT_ID = "883320219445-ejvh51karin9m6dg9mbql56vjn0vp2ls.apps.googleusercontent.com"

# dev (test app) settings (change for production)
FB_APP_ID = "1050879885027789"
FB_APP_SECRET = "826f7fca7e04f05e9d4bae3de5a8e7a2"
FB_APP_SCOPE = "public_profile,email"
