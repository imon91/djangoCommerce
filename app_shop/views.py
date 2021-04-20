
from django.shortcuts import render
from django.views.generic import ListView,DetailView,DeleteView,CreateView

# Create your views here.
from app_shop.models import Product


class index(ListView):
    model = Product
    template_name = 'app_shop/home.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'app_shop/product_detail.html'