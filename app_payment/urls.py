from django.contrib import admin
from django.urls import path

from app_payment import views

app_name = "app_payment"
urlpatterns = [
    path('', views.checkedout, name='checkedout'),
    path('testpayment/', views.testpayment, name='testpayment'),
    path('complete/', views.complete, name='complete'),
    path('purchase/<val_id>/<trans_id>/', views.purchase, name='purchase'),



]
