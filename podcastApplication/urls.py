from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('_dashboard.urls') ),
    path('', include('frontend.urls') ),
    path('', include('account.urls') ),


    # 
    url(r'^media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

