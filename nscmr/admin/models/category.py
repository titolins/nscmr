from nscmr.admin.models.document import Document

class Category(Document):

    __collection__ = 'categories'
    fields = ['name', 'parent', 'ancestors', 'thumbnail', 'header']

    ''' attributtes used by dev class:
    id
    name
    thumbnail
    header_picture
    '''

    def from_form(self):
        return NotImplemented

