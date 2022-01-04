from django import forms
from django.db.models import fields
from django.db.models.query_utils import Q
from django.forms import widgets
# from django.contrib.admin.decorators import display
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget
from django.conf import settings
from .models import *





class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['user','type','format','description','title','file','cover']

    def __init__(self, *args, **kwargs):
        super(PodcastForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.filter(Q(db_table = self._meta.model.__name__))

      

        



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user','type','title','body','thumbnail','description','comment','approve']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.filter(Q(db_table = self._meta.model.__name__))