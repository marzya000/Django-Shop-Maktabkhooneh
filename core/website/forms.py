from django import forms
from website.models import ContactUs,Newsletter



class ContactUsForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    message = forms.CharField(required=True)

    class Meta:
        model = ContactUs
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'message',
        ]


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Newsletter
        fields = ['email']