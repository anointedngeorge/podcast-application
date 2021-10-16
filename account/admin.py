from django.contrib import admin
from django.contrib.admin.sites import AdminSite, site
from django.http import HttpRequest, request
from django.http.response import HttpResponse
from django.urls import path
from django.shortcuts import render
from account.models import Profile
from django.utils import timezone
from datetime import date
import random
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site



@admin.register(Profile)
class AdminProfileUsers(admin.ModelAdmin):
    list_display = ['user', 'logo']
