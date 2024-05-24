from django import forms
from usersapp.models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = fields = ['firstname', 'lastname', 'phone', 'address','image']