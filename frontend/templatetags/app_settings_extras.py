from django import template
from account.models import *
from _admin.models import *
import json
from django.core import serializers
from frontend.gallery import gallery
from django.utils import timezone
import datetime as dt

register = template.Library()

@register.simple_tag
def appsettings(fields):
    try:
        settings = ApplicationSettings.objects.all()
        
        st = serializers.serialize('python', settings)[0].get('fields')
        if fields == 'site_logo' or fields == 'site_favicon':
            return gallery(st.get(fields))
    
        return st.get(fields)

    except Exception as e:
        print(e)


@register.simple_tag
def image(fields):
    try:
        image =  gallery(fields)
        return image
    except:
        pass


@register.simple_tag
def podcastDays(fields):
    d = f"{fields}".split('-')
    dtt = dt.datetime(int(d[0]),int(d[1]),int(d[2])) - dt.datetime.now()
    day = abs(dtt.days)
    if day == 1:
        return 'Today'
    return f"{day} days"