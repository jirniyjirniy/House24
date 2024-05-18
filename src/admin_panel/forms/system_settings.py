# -*- coding: utf-8 -*-
import django.forms as forms

from ..models import *


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields["measure"].empty_label = "Выберите..."

    class Meta:
        model = Service
        fields = "__all__"
        widgets = {"show_in_indication": forms.CheckboxInput(attrs={"class": "rounded-0 shadow-none"})}


ServicesFormset = forms.modelformset_factory(model=Service, form=ServiceForm, can_delete=True, extra=0)


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = "__all__"


MeasureFormset = forms.modelformset_factory(model=Measure, form=MeasureForm, can_delete=True, extra=0)


class TariffForm(forms.ModelForm):
    class Meta:
        model = TariffSystem
        fields = "__all__"


class TariffServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TariffServiceForm, self).__init__(*args, **kwargs)
        self.fields["service"].empty_label = "Выберите..."

    class Meta:
        model = TariffService
        fields = "__all__"

        widgets = {
            "price": forms.TextInput(attrs={}),
            "currency": forms.TextInput(attrs={"disabled": True}),
            "service": forms.Select(attrs={"class": "form-service-selected"}),
        }


TariffServiceFormset = forms.modelformset_factory(model=TariffService, form=TariffServiceForm, can_delete=True, extra=0)


class PaymentDetailForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = "__all__"


class PaymentArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
