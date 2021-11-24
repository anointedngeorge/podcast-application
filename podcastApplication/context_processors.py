
from _admin.models import *

def contestants_videos(request):
    return {
        'contestants_videos': contestant.objects.all().filter(approve = True)
    }