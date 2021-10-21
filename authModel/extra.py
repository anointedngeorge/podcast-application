from typing import Generator
from django.contrib.auth.models import Group
from django.core import serializers
from _admin.models import *
import time



# the roles will be fetched using the group manager database

def group_to_roles():
    try:
        gp = []
        groups = Group.objects.all()
       
        for group in groups:
            if (group.name == "superadmin") or (group.name=="membership") or (group.name=="locked"):
                pass
            else:
                gp.append((group.name, group.name.upper()))
        return gp
    except Exception as e:
        print(e)



    






