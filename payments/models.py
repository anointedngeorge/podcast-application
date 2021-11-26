from django.db import models
# from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
import secrets
from django.conf import settings

from _admin.models import contestant


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, 
    null=True, related_name="paymentcontestant")
    amount = models.FloatField(default=1.00)
    post = models.ForeignKey(contestant, on_delete=models.CASCADE, blank=True, 
    null=True, related_name="userspost")
    reference = models.TextField(default='*******')
    verified = models.BooleanField(default=False)
    data = models.JSONField(blank=True, null=True)
    updated  = models.DateTimeField(default=timezone.now)
    created  = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('-updated',)


    def __str__(self) -> str:
        return f"{self.user.username}-{self.reference}"

