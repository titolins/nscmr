from pymongo import MongoClient


class NsClient(MongoClient):
    """
    Simple MongoClient wrapper class for automatic configuration of the
    client's parameters and acquiring of the correct db handler.
    """
    def __init__(self, app):
        super().__init__(
            host=app.config['MONGO_HOST'],
            port=app.config['MONGO_PORT'])
        self._db_name = app.config.get('MONGO_DB', app.name)

    @property
    def db(self):
        """
        Returns the correct db handler in relation to the app running mode
        (dev, test or production).
        """
        return getattr(self, self._db_name)


def build_db(app):
    """
    Creates the client and returns the db handler.

    NOTE: Perhaps the client wrapper class should be dismissed, considering the
    amount of work and the extra method created just for retrieving it's db
    handler.. Another option is to dismiss this method and get the db when of
    the app's initialization.
    """
    return NsClient(app).db


if __name__ == '__main__':
    from flask import Flask
    test_app = Flask('test')
    test_app.config['DEBUG'] = True
    test_app.config['MONGO_HOST'] = 'localhost'
    test_app.config['MONGO_PORT'] = 27017
    client = NsClient(test_app)
    db = client.db
