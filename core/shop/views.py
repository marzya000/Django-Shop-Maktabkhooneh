from django.shortcuts import render
from django.views.generic import TemplateView

class ShopProductGridView(TemplateView):
    template_name = 'shop/product-grid.html'
