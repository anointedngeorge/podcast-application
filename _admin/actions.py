from django.contrib import admin


# @admin.action(description="Approve Bulk")
def approve_bulk(modelname, request, queryset):
    for queries in queryset:
        queries.approve = True
        queries.save()

# @admin.action(description="Reject Bulk")
def reject_bulk(modelname, request, queryset):
    for queries in queryset:
        queries.approve = False
        queries.save()




