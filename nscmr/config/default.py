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

MUNDIPAGG_KEY = UUID('7075fc55-70ed-41f2-9def-95e5053f11dd')
#MUNDIPAGG_ENDPOINT = 'https://sandbox.mundipaggone.com/'

