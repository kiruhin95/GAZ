from django import forms
from planes.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class UserRegForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'