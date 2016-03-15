from nscmr.admin.models.dev.user import User, UserFactory
from nscmr.admin.models.dev.category import Category, CategoryFactory
from nscmr.admin.models.dev.product import Product, ProductFactory

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
