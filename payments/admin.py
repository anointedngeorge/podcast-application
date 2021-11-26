from django.contrib import admin
from .models import Payment
# Register your models here.


@admin.register(Payment)
class ReferralsAdmin(admin.ModelAdmin):
    search_fields = ("user__startswith",)
    list_display = ("user","reference","amount", "post" ,"verified", "created",)
    list_filter  = ("user",)