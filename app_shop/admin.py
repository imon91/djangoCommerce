from django.contrib import admin


# Register your models here.
from app_shop.models import Category, Product
from loginapp.models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)