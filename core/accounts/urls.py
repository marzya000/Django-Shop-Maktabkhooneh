
from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('',include('django.contrib.auth.urls')),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    # path('register',views.RegisterView.as_view(),name='register'),
    path('password-reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/complete/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]