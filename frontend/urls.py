from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from frontend.views import *

app_name = 'frontend'

urlpatterns = [
    path('', indexpage, name="homepage"),
    path('view-podcast/', view_podcast, name="view-podcast"),
    path('contest/', contest_video, name="contest"),
]
