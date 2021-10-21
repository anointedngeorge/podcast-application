from django.http import request, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from account.forms import userRegistrationForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.conf import settings
from _admin.models import *
from frontend.models import *
from account.models import ApplicationSettings


def indexpage(request):
    context = {}
    context['podcast_lastest'] =  Podcast.objects.all().order_by('upload_at')
    context['podcast'] =  Podcast.objects.all().filter(approve = True)
    context['slider'] =  Sliders.objects.all().filter(approve = True)
    context['profile'] =  Profile.objects.all().filter(approve = True)
    context['category'] =  Category.objects.all().filter(approve = True)
    return render(request, 'klassy/index.html', context=context)