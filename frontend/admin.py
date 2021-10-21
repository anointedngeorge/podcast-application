from django.contrib import admin
from django.forms.models import fields_for_model
from .models import *
from django.contrib import messages
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import os
from _admin.actions import *
# from .forms import *


@admin.register(Sliders)
class FrontendSlider(admin.ModelAdmin):
    list_display = ['title','sub_title','description','bg_image','approve']
    actions = [approve_bulk, reject_bulk]