from django.contrib import admin
from django.urls import path

from app_shop import views

app_name = "app_shop"
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('product_detail/<pk>/', views.ProductDetail.as_view(), name='ProductDetail'),


]
