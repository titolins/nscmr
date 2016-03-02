from nscmr.models.user import User, UserFactory
from nscmr.models.category import Category, CategoryFactory
from nscmr.models.product import Product, ProductFactory

## users
uf = UserFactory()
admin = uf.getAdminUser()
users = [uf.getRegularUser() for i in range(5)]
user = users[0]

## categories
cf = CategoryFactory()
categories = cf.getCategories()

## products
pf = ProductFactory()
products = pf.getProducts()
