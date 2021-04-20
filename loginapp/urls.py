from django.contrib import admin
from django.urls import path

from loginapp import views

app_name = "loginapp"
urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.sing_up, name='sing_up'),
    path('logut_user/', views.logut_user, name='logut_user'),
    path('use_profile/', views.use_profile, name='use_profile'),


]
