
from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('',include('django.contrib.auth.urls')),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    # path('register',views.RegisterView.as_view(),name='register'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('verify/<uidb64>/<token>/',views.VerifyEmailView.as_view(),name='verify_email'),
    path('verification-sent/',views.VerificationSentView.as_view(),name='verification_sent'),
    path('verification-failed/',views.VerificationFailedView.as_view(),name='verification_failed'),

    path('password-reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/complete/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]