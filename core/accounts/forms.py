from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.tasks import send_email
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email",)


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "این ایمیل قبلاً ثبت شده است."
            )

        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "رمز عبور و تکرار آن یکسان نیستند."
            )

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password1"]
        )

        if commit:
            user.save()

        return user


class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("user is not verified")


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

        send_email.delay(
            subject,
            text_message,
            html_message,
            from_email,
            [to_email],
        )