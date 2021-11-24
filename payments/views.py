import requests as req
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import package
from .models import Payment
import uuid
# for enviroment variables 
from decouple import config
from .paystack import Paystack
from users.models import Profile




# Create your views here.

class Package(TemplateView):
    template_name = 'payments/index.html'
    # FOR PAYSTACK PAYMENT 
    PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
    PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uforms'] = package()
        context['PAYSTACK_PUBLIC_KEY'] = self.PAYSTACK_PUBLIC_KEY
        context['PAYSTACK_SECRET_KEY'] = self.PAYSTACK_SECRET_KEY
        context['email'] = self.request.user.email
        context['amount'] = 2200 * 100
        context['token'] = str(uuid.uuid4()).replace("-", "")[:12]
        return context
    
    def get(self, request, *args, **kwargs):
        try:
            if request.user.profile.registration_status ==  True:
                return redirect("/login/")
            return render(request, self.template_name , self.get_context_data())
        except Exception as e:
            return redirect("/") 
    
    def post(self, request, *args, **kwargs):
        form = package(request.POST)
        if form.is_valid():
            if Payment.objects.filter(user = request.user).exists() == False:
                amount = form.cleaned_data.get('payment')
                Payment.objects.create(
                    user = request.user,
                    amount = amount - 200,
                    savings = 200
                ).save()
                return render(request, 'payments/paystack.html', self.get_context_data())
            # 
        return render(request, 'payments/paystack.html', self.get_context_data())


def verify_payment(request, reference:str):
    try:
        verify_payment = Paystack(reference=reference).verify_payment()
        if verify_payment['status'] == True:
            if Payment.objects.filter(user = request.user).exists() == True:
                data = verify_payment['data']
                user_data = Payment.objects.get(user = request.user)
                user_data.verified = True
                user_data.data = data
                user_data.reference = reference
                user_data.save()

                if Profile.objects.filter(user = request.user).exists() == True:
                    users = Profile.objects.get(user = request.user)
                    users.registration_status = True
                    user_data.save()
                    users.save()

                messages.success(request, verify_payment['message'])
                return render(request, 'payments/verification.html')
        else:
            pass
    except Exception as e:
        return redirect('/')
    return HttpResponse('hiiiii')
