from django import forms
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from authModel.models import AppAuthUser
from django.forms.fields import MultipleChoiceField
from .models import *
from django.forms import ClearableFileInput


class userRegistrationForm(UserCreationForm):
    # roles =  MultipleChoiceField(queryset=Category.objects.order_by('name__name', 'name'), opt_group='name')
    email = forms.EmailField(required=True)

    class Meta:
        model = AppAuthUser
        fields = ("username","first_name", "last_name", "email", "password1", "password2", "roles")

    
    def save(self, commit=True):

        try:
            user = super(userRegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.is_staff = True
                user.is_active = True
                user.save()
        
            return user

        except Exception as e:
            print(e)




class GalleryForm(forms.ModelForm):


    class Meta:
        model = Gallary
        fields = ['user', 'file','db_table',]
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


