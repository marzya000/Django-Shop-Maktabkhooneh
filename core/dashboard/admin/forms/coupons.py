from django import forms 
from order.models import CouponModel



class CouponForm(forms.ModelForm):
    class Meta:
        model = CouponModel
        fields = [
            "code", 
            "discount_percent",
            "max_limit_usage", 
            "expiration_date", 
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'form-control'

        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
        # self.fields['discount_percent'].widget.attrs['class'] = 'number'

        self.fields['max_limit_usage'].widget.attrs['class'] = 'form-control'
        # self.fields['max_limit_usage'].widget.attrs['class'] = 'number'

        # self.fields['expiration_date'].widget.attrs['class'] = 'form-control'
        # self.fields['expiration_date'].widget.attrs['class'] = 'datetime-local'
