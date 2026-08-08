from django.contrib import admin
from .models import ContactUs, Newsletter


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'created_at',
    ]

@admin.register(Newsletter)
class Newsletter(admin.ModelAdmin):
    list_display = [
        'email',
        'created_at',
    ]
