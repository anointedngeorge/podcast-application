from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from _dashboard.admin import _dashboard


urlpatterns = [
   path('dashboard/', _dashboard.urls),
]

