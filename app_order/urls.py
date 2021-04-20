from django.contrib import admin
from django.urls import path

from app_order import views

app_name = "app_order"
urlpatterns = [
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('remove_cart_item/<pk>', views.remove_cart_item, name='remove_cart_item'),
    path('increase_product/<pk>', views.increase_product, name='increase_product'),
    path('decrease_product/<pk>', views.decrease_product, name='decrease_product'),



]
