from django.contrib.auth import forms as auth_forms
from django import forms

class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        ## اینو خودت بعدا انجام بده یا نمیدونم چی!!
    }
    pass