# -*- coding: utf-8 -*-
from django import template

from ..models import *

register = template.Library()


@register.filter()
def disablingMeasure(value):
    return Service.objects.filter(measure_id=value).exists()


@register.filter()
def disablingService(value):
    return Receipt.objects.filter(receiptservice__service_id=value).exists()


@register.filter
def get_house_queryset(value):
    flats = FlatOwner.objects.get(id=value).flat_set.all().distinct("house")
    return flats


@register.filter
def get_flat_queryset(value):
    return FlatOwner.objects.get(id=value).flat_set.all()
