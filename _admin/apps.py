from django.apps import AppConfig, apps
from django.core import serializers
import json
import os
import sys
class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '_admin'
    verbose_name = "Lookups"
    model_container = []
    

    def ready(self) -> None:
        dd = apps.get_models()
        for model in dd:
            self.model_container.append((model.__name__, model.__name__))
        

        with open(os.path.join('all_registered_models.py'), 'w')  as ft :
            ft.write(f"modelname = {self.model_container}")
            ft.close()
           


            


    
