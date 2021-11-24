from django import forms
from django.contrib.admin.decorators import display
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.widgets import CheckboxInput, PasswordInput
from .models import Payment





class package(forms.Form):
    payment = forms.CharField(required=True, 
    widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'value':5000}))


