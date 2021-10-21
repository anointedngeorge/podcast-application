from django import forms
from django.db.models import fields
from django.db.models.query_utils import Q
from django.forms import widgets
from django.contrib.admin.decorators import display
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget
from django.conf import settings
from _admin.models import *
from account.models import *




class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['user','type','title','file','cover',]

    def __init__(self, *args, **kwargs):
        super(PodcastForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.filter(Q(db_table = self._meta.model.__name__))
        self.fields['file'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))
        self.fields['cover'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))

      

        
class PodcastExtraForm(forms.ModelForm):
    class Meta:
        model = PodcastExtra
        fields = ['title','file','cover',]

    def __init__(self, *args, **kwargs):
        super(PodcastExtraForm, self).__init__(*args, **kwargs)
        self.fields['file'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))
        self.fields['cover'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user','type','title','body','thumbnail','description','comment']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.filter(Q(db_table = self._meta.model.__name__))
        self.fields['thumbnail'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))




class BlogExtraForm(forms.ModelForm):
    class Meta:
        model = BlogExtra
        fields = ['blog','cover',]

    def __init__(self, *args, **kwargs):
        super(BlogExtraForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','logo',]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['logo'].queryset = Gallary.objects.filter(Q(user = self.current_user, approve = True))