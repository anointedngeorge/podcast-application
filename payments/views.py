from django.urls.base import reverse
import requests as req
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView

from _admin.models import contestant
from .forms import package
from .models import Payment
import uuid
# for enviroment variables 
from decouple import config
from .paystack import Paystack
# from users.models import Profile
from account.models import Profile
from authModel.models import AppAuthUser

import traceback


# Create your views here.

class Package(TemplateView):
    template_name = 'payments/index.html'
    # FOR PAYSTACK PAYMENT 
    PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
    PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
    TOKEN = None
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uforms'] = package()
        context['PAYSTACK_PUBLIC_KEY'] = self.PAYSTACK_PUBLIC_KEY
        context['PAYSTACK_SECRET_KEY'] = self.PAYSTACK_SECRET_KEY
        self.TOKEN = str(uuid.uuid4()).replace("-", "")[:12]
        context['token'] = self.TOKEN
        return context
    
    def get(self, request, *args, **kwargs):
        userdata = AppAuthUser.objects.all().get(pk=int(kwargs.get('userid')))
        context = self.get_context_data()
        context.update({'user':userdata.username})
        context.update({'userid':kwargs.get('userid')})
        context.update({'postid':kwargs.get('postid')})
        return render(request, self.template_name, context=context)

    
    def post(self, request, *args, **kwargs):
        form = package(request.POST)
        if form.is_valid():
            user_id = int(request.POST.get('vuserid'))
            postid = int(kwargs.get('postid'))

            userdata = AppAuthUser.objects.all().get(id=user_id)
            contestant_post = contestant.objects.all().get(id=postid)

            amount = int(form.cleaned_data.get('amount'))
            email = form.cleaned_data.get('email')
            


            context = self.get_context_data()
            context.update({'vuser':userdata})
            context.update({'email':email})
            context.update({'amount':amount})
            context.update({'postid':contestant_post})
            print("This is the amount:", amount)
            param = {
                    'user_id': userdata.id,
                    'amount': amount,
                    'post': contestant_post,
                    'reference': self.TOKEN
                }

            Payment.objects.create(**param)

        return render(request, 'payments/paystack.html', context=context)


def verify_payment(request, reference:str, postid:str):
    """
        data collection 
        * post instance
          - post.user.id
          - post.id
    """
    try:
        verify_payment = Paystack(reference=reference).verify_payment()
        if verify_payment['status'] == True:
            posts = contestant.objects.all().get(id=postid)
            usersData = Payment.objects.all()
            # collect the post database instance
            param = {
                'user_id' : int(posts.user.id),
                'post_id': int(posts.id),
                'reference':str(reference),
            }

            if usersData.filter(**param).exists() == True:
                data = verify_payment['data']
                user_data = usersData.get(**param)
                user_data.verified = True
                user_data.data = data
                # user_data.reference = reference
                user_data.save()
                percentage = (0.1) / 100 * user_data.amount
                posts.vote = percentage
                posts.save()

                messages.success(request, verify_payment['message'])
                return render(request, 'payments/verification.html')
            else:
                print('Failed')
        else:
            return HttpResponse(" Error occurred! ")
    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(e)
        
    return HttpResponse('hiiiii')
