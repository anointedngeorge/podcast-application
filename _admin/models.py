from django.db import models
from django.db.models.enums import Choices, TextChoices
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q, select_related_descend
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from all_registered_models import modelname
from account.models import Gallary


class Category_group(models.Model):
    name = models.CharField(max_length=30)
    approve = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Category Group"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey(Category_group, on_delete=models.CASCADE, null=True, related_name="categoryparent")
    db_table = models.CharField(choices=modelname, max_length = 150, verbose_name="Choose table it belongs", null=True)
    approve = models.BooleanField(default=False)
 
    
    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name


class Status(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="status")
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="podcast")
    # type = models.CharField(max_length = 150, choices=PODCAST_TYPE)
    type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="podcastcategory")
    title = models.CharField(max_length = 150)
    file  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="podcastfile")
    cover  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="podcastcover")
    description = RichTextField(blank=True, null=True)
    approve = models.BooleanField(default=False, verbose_name="Show on website")
    upload_at = models.DateField(auto_now=True,  blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Podcast"

    def __str__(self) -> str:
        return f"{self.title}"


    

   

    


class PodcastExtra(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length = 150)
    file  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="podcastextrafile")
    cover  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="podcastextracover")
    

    class Meta:
        verbose_name_plural = "Podcast extra"


    def __str__(self) -> str:
        return f"{self.title}"
    


# blog section

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length = 150)
    body = RichTextField(blank=True, null=True)
    thumbnail  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="blogthumbnail")
    description = models.CharField(max_length = 150)
    comment = models.TextField(blank=True, null=True)
    upload_at = models.DateField(auto_now=True,  blank=True, null=True)
    
    


    class Meta:
        verbose_name_plural = "Blog Section"


    def __str__(self) -> str:
        return f"{self.user}"




class BlogExtra(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    cover  = models.ForeignKey(Gallary, on_delete=models.CASCADE, null=True, related_name="blogextracover")

    class Meta:
        verbose_name_plural = "Extra Blog Section"


    def __str__(self) -> str:
        return f"{self.blog}"







class ExternalPodcast(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="externalpodcast")
    title = models.CharField(max_length = 150)
    link = models.URLField(max_length = 200, blank=True, null=True)
    # description = models.TextField()
    description = RichTextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    upload_at = models.DateField(auto_now=True,  blank=True, null=True)

    class Meta:
        verbose_name_plural = "External Podcast"


    def __str__(self) -> str:
        return f"{self.title}"