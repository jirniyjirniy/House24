# -*- coding: utf-8 -*-
from django.apps import apps
from django.contrib import admin

business_model = apps.get_app_config("admin_panel").get_models()

for model in business_model:
    admin.site.register(model)
