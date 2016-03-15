########################################################################
#####  Product                     #####################################
########################################################################
#####                                                      #############
#####                                                      #############
#####  Basic product model for development.                #############
#####                                                      #############
#####                                                      #############
#####  Classes:                                            #############
#####     Product                                          #############
#####     ProductFactory                                   #############
#####                                                      #############
#####                                                      #############
#####                                          2016-02-01  #############
#####                                                      #############
########################################################################

from nscmr.admin.models.category import CategoryFactory
from nscmr.admin.helper import slugify

class ProductFactory(object):
    # TODO:
    # Create a getter by category id for products
    def __init__(self):
        cf = CategoryFactory()
        self.name = 'Lençol com estampa florida c/ tecido importado'
        self.description = '''
                FEITO COM PERCAL 7000 FIOS DA ÍNDIA ORIENTAL
                IDEAL PARA CASAS DE CAMPO, SÍTIOS, FAZENDAS ETC.
            '''
        self.price = 450.00
        self.size = "3.50m x 2.50m"
        self.thumbnail = "http://placehold.it/400x300"
        self.background_picture = "http://placehold.it/1920x1080"
        self.category = cf.getCategories()[0]

    def getProducts(self):
        return [
                Product(
                    id_ = i,
                    name = self.name,
                    description = self.description,
                    price = self.price,
                    size = self.size,
                    thumbnail = self.thumbnail,
                    background_picture = self.background_picture,
                    category = self.category) \
                for i in range(8)]


class Product(object):
    def __init__(self, id_, name, description, price, size, thumbnail,
            background_picture, category):
        self.id_ = id_
        self.name = name
        self.description = description
        self.price = price
        self.size = size
        self.thumbnail = thumbnail
        self.background_picture = background_picture
        self.category = category

    @property
    def slug(self):
        return slugify(self.name)


if __name__ == '__main__':
    pass
