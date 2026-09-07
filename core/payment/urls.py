from django.urls import path,re_path
from . import views

app_name = 'payment'

urlpatterns = [
    path('verify',views.PaymentVerifyView.as_view(),name='verify'),
    path('zibal/verify',views.ZibalPaymentVerifyView.as_view(),name='zibal_verify'),
]