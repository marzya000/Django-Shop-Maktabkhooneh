from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed
from .models import ReviewModel
from .forms import SubmitReviewForm
from django.contrib import messages


class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = ReviewModel
    form_class = SubmitReviewForm
  
    def form_valid(self, form):
        product= form.changed_data['product']
        messages.success(self.request, 'دیدگاه شما با موفقیت ثبت شد و پس از بررسی نمایش داده خواهد شد')        
        return redirect(reverse_lazy('shop:product-detail', kwargs={'slug':product.slug}))

    def form_invalid(self, form):
        product= form.changed_data['product']
        messages.error(self.request, 'خطایی در ثبت دیدگاه اتفاق افتاد')        
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)
