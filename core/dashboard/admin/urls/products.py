from django.urls import path,include
from .. import views


urlpatterns = [
    # Product list URL
    path('product/list/',views.AdminProductListView.as_view(),name='product-list'),
    # Product creation URL
    path('product/create/',views.AdminProductCreateView.as_view(),name='product-create'),
    # Product edit URL
    path('product/<int:pk>/edit/',views.AdminProductEditView.as_view(),name='product-edit'),
    # Product deletion URL
    path('product/<int:pk>/delete/',views.AdminProductDeleteView.as_view(),name='product-delete'),
    # Additional product image deletion URL
    path('product/images/<int:pk>/delete/',views.AdminProductImageDeleteView.as_view(),name='product-image-delete'),
]