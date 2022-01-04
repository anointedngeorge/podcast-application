from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.contrib import admin
# from django.contrib.admin.decorators import action
from django.utils.translation import activate
from _admin.models import *
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from account.models import *
from django.urls import path, include
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import os
import sys
from _dashboard.forms import *
# from the admin import all forms
from account.forms import *


class PodastCustomDashboard(admin.AdminSite):
    site_header = "User Dashboard"
    site_title = "User's dashboard"
    index_title = "My Dashboard"

_dashboard = PodastCustomDashboard(name="my admin dashboard")



class userProfile(admin.ModelAdmin):
      exclude = ['user']
      list_display = ['user', 'logo']
      form = ProfileForm


      def get_form(self, request, obj, **kwargs):
        form = super(userProfile, self).get_form(request, **kwargs)
        form.current_user = request.user
        return form


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
    form = BlogExtraForm
    


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title']
    exclude = ['user']
    form = BlogForm
    inlines = [BlogExtraAdmin]


    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            inline.form.current_user = request.user
            yield inline.get_formset(request, obj), inline


    def get_form(self, request, obj, **kwargs):
        form = super(BlogAdmin, self).get_form(request, **kwargs)
        form.current_user = request.user
        return form


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)

   


    def save_model(self, request, obj, form, change) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)


_dashboard.register(Blog, BlogAdmin)



class PodcastExtraAdmin(admin.TabularInline):
    model = PodcastExtra
    form = PodcastExtraForm

    


# custom action
# admin.action(description="export as json")
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

class PodcastAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title','file','cover',]
    exclude = ['user']
    form = PodcastForm
    inlines = [PodcastExtraAdmin]
    actions = [export_as_json]   

    # for inline forms
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            inline.form.current_user = request.user
            yield inline.get_formset(request, obj), inline


    def get_form(self, request, obj, **kwargs):
        form = super(PodcastAdmin, self).get_form(request, **kwargs)
        form.current_user = request.user
        return form



    def get_urls(self):
        urls = super().get_urls()
        new_url = [
            path('activate-membership/', self.activate_membership)
        ]
        return new_url + urls


    def activate_membership(self, request): 
        return render(request, 'admin/activate_membership.html')
      

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)


    def save_model(self, request, obj, form, change) -> None:
        try:
            obj.user = request.user
            limit_status = obj.user.status
            db_table = self.model.objects.all().filter(user = request.user)
            if limit_status.status == False:
                if (len(db_table) < int(limit_status.limit)):
                    return super().save_model(request, obj, form, change)

            elif limit_status.status:
                return super().save_model(request, obj, form, change)
            
            
            link = "<a href='activate-membership/'>Activate Membership</a>"
            messages.add_message(request, messages.ERROR,  format_html(f'Your free account allows {limit_status.limit} uploads. Please Upgrade to {link} package to enjoy more features.'))
        except Exception as e:
            messages.add_message(request, messages.WARNING, f"{e}" )
  



_dashboard.register(Podcast, PodcastAdmin)



class ExternalPodcastAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','title','link','description']
    exclude = ['user']


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)

    
    def save_model(self, request, obj, form, change) -> None:
        obj.user = request.user
        limit_status = obj.user.status
        db_table = self.model.objects.all().filter(user = request.user)
        if limit_status.status == False:
            if (len(db_table) < int(limit_status.limit)):
                return super().save_model(request, obj, form, change)

        elif limit_status.status:
            return super().save_model(request, obj, form, change)
      
        
        link = "<a href='activate-membership/'>Activate Membership</a>"
        messages.add_message(request, messages.ERROR,  format_html(f'Your free account allows {limit_status.limit} uploads. Please Upgrade to {link} package to enjoy more features.'))

_dashboard.register(ExternalPodcast, ExternalPodcastAdmin)





class GallerySettingsUser(admin.ModelAdmin):
    search_fields = ['user__startwith']
    list_display = ['user','file','db_table','approve','upload_at']
    exclude = ['user']
    form = GalleryForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return self.model.objects.all().filter(user=request.user)

        

    def delete_queryset(self, request, queryset) -> None:
        for qs in queryset:
            if (os.path.exists(f"{settings.MEDIA_ROOT}/{qs.file}")):
                os.unlink(f"{settings.MEDIA_ROOT}/{qs.file}")
        return super().delete_queryset(request, queryset)


    def save_model(self, request, obj, form, change) -> None:
        data = request.FILES.getlist('file')
        for file in data:
            self.model.objects.create(
                user = request.user,
                file = file,
                db_table = obj.db_table
            )


_dashboard.register(Gallary, GallerySettingsUser)