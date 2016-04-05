from .config import Config

class ProductionConfig(Config):
    # update this when db is ready
    # DATABASE_URI = ""
    MONGO_DB = 'nscmr'
