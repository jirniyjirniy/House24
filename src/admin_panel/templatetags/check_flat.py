# -*- coding: utf-8 -*-
from django import template

from src.admin_panel.models import *

register = template.Library()


@register.filter
def accept_flat_payment(value):
    result = True
    flat = Flat.objects.get(pk=value)

    if hasattr(flat, "personal_account"):
        if flat.personal_account == "" or flat.personal_account is None:
            result = False
    else:
        result = False
    return result
