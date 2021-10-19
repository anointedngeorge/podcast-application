from django.contrib import admin
from .models import *
from django.conf import settings
import os




admin.site.index_title = "Podcast super user"
admin.site.site_header = "Super Administrator"
admin.site.site_title = "Demtgfamily Podcast Application"




@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass



# add extra fields to podcast
class PodcastExtraAdmin(admin.TabularInline):
    model = PodcastExtra
    

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ['title_startwith',]
    list_display = ['user','type','title','file','cover',]
    inlines = [PodcastExtraAdmin]


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
    list_display = ['user','type','title','file','cover',]
    inlines = [BlogExtraAdmin]


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
