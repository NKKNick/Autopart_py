from django import forms
from userinterface.models import product as Product
from worker_app.models import Worker


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"
