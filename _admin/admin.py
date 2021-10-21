from django.contrib import admin
from django.forms.models import fields_for_model
from .models import *
from django.contrib import messages
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import os
from .forms import *
from _admin.actions import *





admin.site.index_title = "Podcast super user"
admin.site.site_header = "Super Administrator"
admin.site.site_title = "Demtgfamily Podcast Application"




@admin.register(Category_group)
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'db_table','approve']
    actions = [approve_bulk, reject_bulk]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass



# add extra fields to podcast
class PodcastExtraAdmin(admin.TabularInline):
    model = PodcastExtra
    

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title','description','file','cover','approve']
    # fields are defined in the PodcastForm form section
    form = PodcastForm
    inlines = [PodcastExtraAdmin]
    actions = [approve_bulk, reject_bulk]
    

    def save_model(self, request, obj, form, change) -> None:
        if obj.user.is_superuser:
            return super().save_model(request, obj, form, change)
        else:
            limit_status = obj.user.status
            db_table = self.model.objects.all().filter(user = obj.user)
            if limit_status.status == False:
                if (len(db_table) < int(limit_status.limit)):
                    return super().save_model(request, obj, form, change)

            elif limit_status.status:
                return super().save_model(request, obj, form, change)
            
            messages.add_message(request, messages.ERROR,  format_html(f'{obj.user} is operating a free account, and has reached maximum upload limit of ({ limit_status.limit })'))






@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ['user_startwith']
    list_display = ['user','status', 'limit']




@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass






# add extra fields to podcast
class BlogExtraAdmin(admin.TabularInline):
    model = BlogExtra
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title',]
    form =  BlogForm
    inlines = [BlogExtraAdmin]
