from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from accounts.forms import AuthenticationForm, CustomPasswordResetForm, SignupForm
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from accounts.tasks import send_email
from django.shortcuts import redirect
from accounts.models import User
from django.views.generic import TemplateView



class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm  
    success_url = reverse_lazy("accounts:verification_sent")

    def form_valid(self, form):
        user = form.save()

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        verification_path = reverse(
            "accounts:verify_email",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )

        verification_url = (
            self.request.build_absolute_uri(
                verification_path
            )
        )

        context = {
            "user": user,
            "verification_url": verification_url,
        }

        subject = render_to_string(
            "emails/verification_subject.txt",
            context,
        )

        subject = "".join(
            subject.splitlines()
        )

        html_message = render_to_string(
            "emails/verification_email.html",
            context,
        )

        text_message = strip_tags(
            html_message
        )

        send_email.delay(
            subject,
            text_message,
            html_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return super().form_valid(form)



class VerifyEmailView(View):

    def get(self, request, uidb64, token):

        try:
            uid = force_str(
                urlsafe_base64_decode(uidb64)
            )

            user = User.objects.get(pk=uid)

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            user = None

        if (
            user is not None
            and default_token_generator.check_token(
                user,
                token,
            )
        ):
            user.is_verified = True

            user.save(
                update_fields=["is_verified"]
            )

            login(request, user)

            return redirect("/")

        return redirect(
            "accounts:verification_failed"
        )


class VerificationSentView(TemplateView):
    template_name = ("accounts/verification_sent.html") 


class VerificationFailedView(TemplateView):
    template_name = ("accounts/verification_failed.html")


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = CustomPasswordResetForm
    email_template_name = "emails/password_reset_email.html"
    subject_template_name = "emails/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"



class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
