from nscmr.admin.models.document import Document

class Category(Document):
    __collection__ = 'categories'

    ''' attributtes used by dev class:
    id
    name
    thumbnail
    header_picture
    '''

