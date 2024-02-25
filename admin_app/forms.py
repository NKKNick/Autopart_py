from django import forms
from userinterface.models import product as Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"