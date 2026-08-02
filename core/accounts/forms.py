from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.tasks import send_password_reset_email




class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        # if not user.is_verified:
        #     raise ValidationError("user is not verified")


class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        
        subject = render_to_string(
            subject_template_name,
            context
        )

        subject = "".join(subject.splitlines())

        html_message = render_to_string(
            email_template_name,
            context
        )

        text_message = strip_tags(html_message)

        send_password_reset_email.delay(
            subject,
            text_message,
            html_message,
            from_email,
            [to_email],
        )