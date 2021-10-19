from django.conf import settings
from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.decorators import action
from django.utils.translation import activate
from _admin.models import *
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from account.models import Profile
from django.urls import path, include
from django.utils.translation import gettext as _
import os
import sys


class PodastCustomDashboard(admin.AdminSite):
    site_header = "User Dashboard"
    site_title = "User's dashboard"
    index_title = "My Dashboard"

_dashboard = PodastCustomDashboard(name="my admin dashboard")



class userProfile(admin.ModelAdmin):
      exclude = ['user']
      list_display = ['user', 'logo']

      def save_model(self, request, obj, form, change) -> None:
          obj.user  =  request.user
          return super().save_model(request, obj, form, change)


      def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.logo}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.logo}")
        return super().delete_queryset(request, queryset)

_dashboard.register(Profile, userProfile)




class userStatus(admin.ModelAdmin):
    search_fields = ['user_startwith']
    exclude = ['user']
    list_display = ['user','status', 'limit']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)
_dashboard.register(Status, userStatus)





# add extra fields to podcast
class BlogExtraAdmin(admin.TabularInline):
    model = BlogExtra
    


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title','file','cover',]
    exclude = ['user']
    inlines = [BlogExtraAdmin]


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)

    def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.file}")) and (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.cover}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.file}")
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.cover}")
                # this will fetch the inlines in the index 0 and append the model to it
                # which for this case is PodcastExtra
                inline_tb = self.inlines[0].model.objects.all().filter(blog = qs)
                for inline in inline_tb:
                    if (os.path.exists(f"{settings.MEDIA_ROOT}/{inline.cover}")):
                        os.unlink(f"{settings.MEDIA_ROOT}/{inline.cover}")
        return super().delete_queryset(request, queryset)


    def save_model(self, request, obj, form, change) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)


_dashboard.register(Blog, BlogAdmin)



class PodcastExtraAdmin(admin.TabularInline):
    model = PodcastExtra
    


# custom action
@admin.action(description="export as json")
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

class PodcastAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title','file','cover',]
    exclude = ['user']
    inlines = [PodcastExtraAdmin]
    actions = [export_as_json]   

    def get_urls(self):
        urls = super().get_urls()
        new_url = [
            path('activate-membership/', self.activate_membership, name="activate-memebership")
        ]
        return urls + new_url


    def activate_membership(self, request):
     
        return HttpResponse('Membership activated')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)

   
    def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.file}")) and (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.cover}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.file}")
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.cover}")
                # this will fetch the inlines in the index 0 and append the model to it
                # which for this case is PodcastExtra
                inline_tb = self.inlines[0].model.objects.all().filter(podcast = qs)
                for inline in inline_tb:
                    if (os.path.exists(f"{settings.MEDIA_ROOT}/{inline.file}")) and (os.path.exists(f"{settings.MEDIA_ROOT}/{inline.cover}")):
                        os.unlink(f"{settings.MEDIA_ROOT}/{inline.file}")
                        os.unlink(f"{settings.MEDIA_ROOT}/{inline.cover}")
        return super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change) -> None:
        obj.user = request.user
        limit_status = obj.user.status
        db_table = self.model.objects.all().filter(user = request.user)
        if limit_status.status == False:
            if (len(db_table) < int(limit_status.limit)):
                return super().save_model(request, obj, form, change)

        elif limit_status.status:
            return super().save_model(request, obj, form, change)
        link = "<a href={% url 'activate-memebership' %}>Activate Membership</a>"
        messages.add_message(request, messages.ERROR,  f'Your free account allows {limit_status.limit} uploads. Please Upgrade to {link} package to enjoy more features ')



_dashboard.register(Podcast, PodcastAdmin)