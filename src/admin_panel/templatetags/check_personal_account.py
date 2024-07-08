from django import template
from ..models import *

register = template.Library()


@register.filter
def accept_payment(value):
    result = True
    personal_account = PersonalAccount.objects.get(pk=value)
    if personal_account.status == "disabled" or personal_account.flat is None:
        result = False

    return result
