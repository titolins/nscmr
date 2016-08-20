import os
from uuid import UUID

basedir = '/home/snil/dev/nscmr'

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'instance/uploads')
#UPLOADS_IMAGES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'img/')

DEBUG = True
TESTING = False

SUPPORT_CONTACT = 'contato@studioduvet.com.br'
MONGODB_DB = 'nscmr_dev'

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = MONGODB_DB

# sandbox
PAGSEGURO_TOKEN = "41224F4E00B840BEBD649FE0569333A6"
PAGSEGURO_ENDPOINT = "https://ws.sandbox.pagseguro.uol.com.br/v2/checkout/"
PAGSEGURO_SESSIONS_EP = "https://ws.sandbox.pagseguro.uol.com.br/v2/sessions/"

GOOGLE_CLIENT_ID = "883320219445-ejvh51karin9m6dg9mbql56vjn0vp2ls.apps.googleusercontent.com"

# dev (test app) settings (change for production)
FB_APP_ID = "1050879885027789"
FB_APP_SECRET = "826f7fca7e04f05e9d4bae3de5a8e7a2"
FB_APP_SCOPE = "public_profile,email"
