from django.contrib import admin
from django.contrib.admin.sites import AdminSite, site
from django.http import HttpRequest, request
from django.http.response import HttpResponse
from django.urls import path
from django.shortcuts import render
from account.models import *
from account.forms import *
from django.utils import timezone
from datetime import date
import random
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import os
from _admin.actions import *

@admin.register(Profile)
class AdminProfileUsers(admin.ModelAdmin):
    list_display = ['user', 'logo', 'approve']
    actions = [approve_bulk, reject_bulk]

    def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.logo}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.logo}")
        return super().delete_queryset(request, queryset)







@admin.register(ApplicationSettings)
class GeneralSettings(admin.ModelAdmin):
    search_fields = ['site_title__startwith']
    list_display = ['site_title','tagline_title','site_descriptions','site_logo','site_favicon']




@admin.register(Gallary)
class GallerySettings(admin.ModelAdmin):
    search_fields = ['user__startwith']
    list_display = ['user','file','db_table','approve', 'upload_at']
    form = GalleryForm
    actions = [approve_bulk, reject_bulk]

    def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.file}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.file}")
        return super().delete_queryset(request, queryset)


    def save_model(self, request, obj, form, change) -> None:
        data = request.FILES.getlist('file')
        for file in data:
            self.model.objects.create(
                user = obj.user,
                file = file,
                db_table = obj.db_table
            )
            
       






@admin.register(EmailSettings)
class EmailSettings(admin.ModelAdmin):
    search_fields = ['protocol__startwith']
    list_display = ['protocol','smtp_username','smtp_password','smtp_security','smtp_port']