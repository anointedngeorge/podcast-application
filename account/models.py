from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from authModel.models import AppAuthUser

from all_registered_models import modelname


class Gallary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
     related_name="gallery")
    file = models.FileField(upload_to="galleries", null=True)
    db_table = models.CharField(max_length = 150, choices=modelname)
    approve = models.BooleanField(default=False, null=True, verbose_name="Make this image visible")
    upload_at = models.DateField(auto_now=True, null=True, verbose_name="Upload Date")
    
    

    class Meta:
        verbose_name_plural = "Gallery"

    def __str__(self) -> str:
        return f"{self.file}"

        
    



class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
     related_name="profile")
    logo = models.ForeignKey(Gallary, on_delete=models.CASCADE, related_name='profilegallery', null=True)
    approve = models.BooleanField(default=False, null=True, verbose_name="Show on website")
    
    
    verbose_name="Profile logo"
    

    class Meta:
        verbose_name_plural = "Profile Settings"
        

    def __str__(self) -> str:
        return f"{self.user}"




class ApplicationSettings(models.Model):
    site_title = models.CharField(max_length=100, blank=True, null=True, default='')
    tagline_title = models.CharField(max_length = 150, null=True)
    site_descriptions = models.TextField(blank=True, null=True)
    site_logo =  models.ForeignKey(Gallary, on_delete=models.CASCADE, related_name='sitelogo', null=True)
    site_favicon =  models.ForeignKey(Gallary, on_delete=models.CASCADE, related_name='sitefaviconlogo', null=True)
    google_analytics  = models.TextField(blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "General App Settings"
        

    def __str__(self) -> str:
        return f"{self.site_title}"





class EmailSettings(models.Model):

    EMAIL_SECURITY = [('TLS','TLS'), ('SSL','SSL'), ('False','False')]

    protocol = models.CharField(max_length=100, blank=True, null=True, default='')
    smtp_host = models.CharField(max_length=100, blank=True)
    smtp_username  = models.CharField(max_length = 150, blank=True)
    smtp_security  = models.CharField(choices=EMAIL_SECURITY, max_length = 150, blank=True)
    smtp_port  = models.IntegerField(blank=True, null=True)
    smtp_password  = models.CharField(max_length = 150, blank=True)


    def __str__(self) -> str:
        return f'{self.smtp_host}'