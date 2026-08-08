from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from website.forms import ContactUsForm, NewsletterForm
from .models import ContactUs, Newsletter
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterForm()
        return context


# class ContactView(TemplateView):
#     template_name = 'website/contact.html'


class AboutView(TemplateView):
    template_name = 'website/about.html'

class ContactView(CreateView):
    model = ContactUs
    template_name = 'website/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('website:contact')


class NewsletterView(CreateView):
    model = Newsletter
    template_name = 'website/index.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('website:index')


