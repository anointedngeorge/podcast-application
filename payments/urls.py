from django.urls import path
from . import views
from .views import Package


app_name = "payments"

urlpatterns = [
    path('package/<int:postid>/<int:userid>/', Package.as_view(), name='package'),
    path('verify/<str:reference>/<int:postid>/', views.verify_payment, name='verify'),
]
