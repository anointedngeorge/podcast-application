from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from _admin.models import Status



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        # print('Created ...')
        Profile.objects.create(user=instance)
        Status.objects.create(user=instance)