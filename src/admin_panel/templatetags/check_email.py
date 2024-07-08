from django import template
from ..models import *

register = template.Library()


@register.filter
def accept_email(value):
    result = True
    receipt = Receipt.objects.get(pk=value)
    if receipt.flat.flat_owner is None:
        result = False
    return result
