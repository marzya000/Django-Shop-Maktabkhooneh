from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django.contrib import messages
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.db.models import Sum
from shop.models import ProductModel,ProductStatusType
from order.models import OrderStatusType




class IndexView(TemplateView):
    template_name = 'website/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        best_selling_products = (
            ProductModel.objects
            .filter(
                order_items__order__status=OrderStatusType.success.value
            )
            .annotate(
                total_sold=Sum("order_items__quantity")
            )
            .order_by("-total_sold")[:3]
        )

        best_products = (
            ProductModel.objects
            .filter(
                status=ProductStatusType.publish.value,
                avg_rate__gt=0
            )
            .prefetch_related("images")
            .order_by("-avg_rate")[:3]
        )

        context["best_selling_products"] = best_selling_products
        context["best_products"] = best_products

        return context


class ContactView(TemplateView):
    template_name = 'website/contact.html'



class AboutView(TemplateView):
    template_name = 'website/about.html'

