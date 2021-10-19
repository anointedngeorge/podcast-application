from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


PODCAST_TYPE = [
    ('VID', 'VIDEO'),
    ('AUD', 'AUDIO')
]

MEDIA_TYPE = [
      ('VID', 'VIDEO'),
      ('AUD', 'AUDIO')
]



class Status(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False) # False = free account, True = Membership account or paid account
    limit = models.IntegerField(default=5)
    
    


    class Meta:
        verbose_name_plural = "Status"


    def __str__(self) -> str:
        return f"{self.user}"
    
    



class Package(models.Model):
     name = models.CharField(max_length = 150)
     code = models.CharField(max_length = 150)
     amount = models.BigIntegerField()
     duration = models.DateField(auto_now=False, blank=True, null=True)


     class Meta:
        verbose_name_plural = "Package"


     def __str__(self) -> str:
        return f"{self.name}"
     
     
     


class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True)
    expiration = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now=True,  blank=True, null=True)




    class Meta:
        verbose_name_plural = "Membership"


    def __str__(self) -> str:
        return f"{self.user}"
    
    
    



class Podcast(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length = 150, choices=PODCAST_TYPE)
    title = models.CharField(max_length = 150)
    file = models.FileField(upload_to="file")
    cover = models.ImageField(upload_to="cover")
    description = models.TextField()
    approved = models.BooleanField(default=False)
    
    upload_at = models.DateField(auto_now=True,  blank=True, null=True)
    
    


    class Meta:
        verbose_name_plural = "Podcast"


    def __str__(self) -> str:
        return f"{self.title}"
    
    
    


class PodcastExtra(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length = 150)
    file = models.FileField(upload_to="extrafile")
    cover = models.ImageField(upload_to="extracover")
    

    class Meta:
        verbose_name_plural = "Podcast extra"


    def __str__(self) -> str:
        return f"{self.title}"
    


# blog section

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length = 150, choices=MEDIA_TYPE)
    title = models.CharField(max_length = 150)
    file = models.FileField(upload_to="blogfile")
    cover = models.ImageField(upload_to="blogcover")
    description = models.CharField(max_length = 150)
    comment = models.TextField()
    upload_at = models.DateField(auto_now=True,  blank=True, null=True)
    
    


    class Meta:
        verbose_name_plural = "Blog Section"


    def __str__(self) -> str:
        return f"{self.user}"




class BlogExtra(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    cover = models.ImageField(upload_to="extrablogcover", verbose_name="Extra Images ")
   

    class Meta:
        verbose_name_plural = "Extra Blog Section"


    def __str__(self) -> str:
        return f"{self.blog}"