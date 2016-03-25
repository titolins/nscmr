from nscmr.admin.models.document import Document

class Category(Document):

    __collection__ = 'categories'
    fields = ['name', 'slug', 'parent', 'ancestors', 'thumbnail', 'header']

    ''' attributtes used by dev class:
    id
    name
    thumbnail
    header_picture
    '''

    @staticmethod
    def from_form(form_data):
        return NotImplemented

