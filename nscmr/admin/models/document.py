# structure inspired by MongoKit, however alot simpler (and supporting
# python3)

from bson import InvalidDocument

# import db so we have access to the collections through the models
from nscmr import db

class DocumentProperties(type):
    """
    Document metaclass for acquiring the collection handler automatically.
    """
    def __new__(cls, name, parents, dct):
        if '__collection__' in dct:
            # get the collection name and set the handler from the db
            dct['collection'] = db[dct['__collection__']]
        return super(DocumentProperties, cls).__new__(cls, name, parents, dct)


class Document(object, metaclass=DocumentProperties):
    '''
    Base document class/interface for pymongo
    '''
    required_fields = None
    validators = None

    def __init__(self, content):
        self.content = content

    @staticmethod
    def from_form(self):
        return NotImplemented

    @classmethod
    def get_by_id(cls, doc_id):
        return cls(cls.collection.find_one({'_id': doc_id}))

    def validate(self):
        # validates existence of fields first
        if self.required_fields is not None:
            for field in self.required_fields:
                if field not in self.content:
                    raise InvalidDocument("Campo necessário '{}' não existe".\
                            format(field))
        # apply actual validators
        if self.validators is not None:
            for field in self.validators:
                if not self.validators[field][0](self.content[field]):
                    raise InvalidDocument(self.validators[field][1])

    def get_id(self):
        return str(self.content['_id'])

    def save(self):
        return NotImplemented


