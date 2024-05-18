# -*- coding: utf-8 -*-
import sys

from django.urls import resolve

from src.admin_panel.models import Personal, Role


def user_info(request):
    app_name = sys.modules[resolve(request.path_info).func.__module__].__package__
    context = {}
    if app_name == "cabinet":
        context = {}
    elif app_name == "src.admin_panel.views":
        user_permissions = Role.objects.get(name=Personal.objects.get(user_id=request.user.id).role)
        context = {
            "user_permission": user_permissions,
        }
    elif app_name == "website":
        pass
    elif app_name == "accounts":
        pass
    return context
