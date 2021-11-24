from django.db import models
# from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
import secrets
from django.conf import settings


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, 
    null=True, related_name="paymentcontestant")
    amount = models.FloatField(default=1.00)
    savings = models.FloatField(default=1.00)
    reference = models.TextField(default='*******')
    refund = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    data = models.JSONField(blank=True, null=True)
    updated  = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)


    def __str__(self) -> str:
        return f"{self.user.username}-{self.reference}"

