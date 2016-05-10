from pymongo import MongoClient
from .models import User, Category, Product, Variant


class NsClient(MongoClient):
    """
    Simple MongoClient wrapper class for automatic configuration of the
    client's parameters and acquiring of the correct db handler.
    """
    def __init__(self, app):
        super().__init__(
            host=app.config['MONGODB_HOST'],
            port=app.config['MONGODB_PORT'])
        self._db_name = app.config.get('MONGODB_DB', app.name)
        self.collections = {}

    @property
    def db(self):
        """
        Returns the correct db handler in relation to the app running mode
        (dev, test or production).
        """
        return getattr(self, self._db_name)

    def register_collection(self, document):
        if hasattr(document, '__collection__'):
            # set the collection handler
            document.collection = self.db[getattr(document, '__collection__')]
            # create indexes
            document.create_indexes()


def build_db(app):
    """
    Creates the client and returns the db handler.

    NOTE: Perhaps the client wrapper class should be dismissed, considering the
    amount of work and the extra method created just for retrieving it's db
    handler.. Another option is to dismiss this method and get the db when of
    the app's initialization.
    """
    documents = [User, Category, Product, Variant]
    client = NsClient(app)
    for d in documents:
        client.register_collection(d)
    return client.db

