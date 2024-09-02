from django import forms
from .models import Product

class OrderForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
