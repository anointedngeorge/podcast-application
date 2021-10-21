from django.db import models
from django.db.models.enums import Choices
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q, select_related_descend
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from all_registered_models import modelname
from account.models import *




class Sliders(models.Model):
    title = models.CharField(max_length = 150, null=True)
    sub_title = models.CharField(max_length = 150, null=True, blank=True)
    description = models.TextField()
    bg_image = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, verbose_name="Background Image Cover")
    approve = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Add Slider"
    

    def __str__(self) -> str:
        return f"{self.title}"



class Advertisement(models.Model):
    api_link = models.URLField(max_length = 200, verbose_name="Enter Api Link")
    



class Contact(models.Model):
    pass


class About(models.Model):
    title = models.CharField(max_length = 150, blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    


class Footer(models.Model):
    pass