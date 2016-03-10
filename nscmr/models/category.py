########################################################################
#####  Category                    #####################################
########################################################################
#####                                                      #############
#####                                                      #############
#####  Memory models for category class.                   #############
#####  For development only.                               #############
#####                                                      #############
#####  Classes:                                            #############
#####     Category                                         #############
#####     CategoryFactory                                  #############
#####                                                      #############
#####                                          2016-01-30  #############
#####                                                      #############
########################################################################

from nscmr.helper import slugify


class CategoryFactory(object):
    def __init__(self):
        self.names = {
                'Duvets': 3,
                'Lençois': 1,
                'Colchas': 4,
                'Peseiras': 5,
                'Toalhas de mesa': 6,
                'Acessórios': 2,
        }
        self.thumbnail = "http://placehold.it/400x300"
        self.header_picture = "http://placehold.it/1400x400"

    def getCategories(self):
        return [
                Category(
                    c_id = v,
                    name = k,
                    thumbnail = self.thumbnail,
                    header_picture = self.header_picture) \
                for k,v in self.names.items()]


class Category(object):
    def __init__(self, c_id, name, thumbnail, header_picture):
        self.id_ = c_id
        self.name = name
        self.thumbnail = thumbnail
        self.header_picture = header_picture

    @property
    def slug(self):
        return slugify(self.name)

if __name__ == '__main__':
    cf = CategoryFactory()
    cf.getCategories()
