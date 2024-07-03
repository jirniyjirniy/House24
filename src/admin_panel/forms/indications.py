# -*- coding: utf-8 -*-
import django.forms as forms

from src.admin_panel.models import Flat, House, Indication, Section, Service


class IndicationForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={"class": "number ignore", "placeholder": ""}), label='')
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        label="Секция",
        required=False,
        widget=forms.Select(attrs={"class": "form-section-select"}),
    )
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        label="Дом",
        required=False,
        widget=forms.Select(attrs={"class": "form-house-select"}),
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(show_in_indication=True),
        label="Счетчик",
        widget=forms.Select(attrs={"class": "form-service-select"}),
    )
    flat = forms.ModelChoiceField(
        queryset=Flat.objects.all(),
        label="Квартира",
        widget=forms.Select(attrs={"class": "form-flat-select"}),
    )
    date_published = forms.DateField(
        label="",
        widget=forms.DateInput(attrs={"class": "publishing-date ignore", "placeholder": ""}),
    )

    def __init__(self, *args, **kwargs):
        super(IndicationForm, self).__init__(*args, **kwargs)
        self.fields["house"].empty_label = "Выберите..."
        self.fields["section"].empty_label = "Выберите..."
        self.fields["flat"].empty_label = "Выберите..."
        self.fields["service"].empty_label = "Выберите..."
        self.fields["date_published"].empty_label = "Выберите..."

    class Meta:
        model = Indication
        fields = "__all__"
        widgets = {
            "indication_val": forms.NumberInput(attrs={"placeholder": ""}),
        }


class IndicationsFilterForm(forms.Form):
    house = forms.ModelChoiceField(
        label="",
        required=False,
        queryset=House.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0 form-house-select",
            }
        ),
    )
    section = forms.ModelChoiceField(
        label="",
        required=False,
        queryset=Section.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control select2-simple-section select2-success rounded-0 form-section-select"}
        ),
    )

    flat = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
    service = forms.ModelChoiceField(
        label="",
        required=False,
        queryset=Service.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control select2-simple select2-success rounded-0 form-service-select"}
        ),
    )


class CounterIndicationsFilterForm(forms.Form):
    STATUS_CHOICE = (
        ("", ""),
        ("new", "Новое"),
        ("considered", "Учтено"),
        ("considered and paid", "Учтено и оплачено"),
        ("null", "Нулевое"),
    )
    number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
        label="",
        required=False,
        max_length=100,
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICE,
        label="",
        widget=forms.Select(
            attrs={
                "class": "form-control select2-simple select2-success rounded-0",
                "placeholder": "",
            }
        ),
        required=False,
    )
    daterange = forms.CharField(
        widget=forms.DateInput(attrs={"placeholder": "", "class": "daterange", "value": ""}),
        label="",
        required=False,
    )
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0 form-house-select",
            }
        ),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0 form-section-select",
            }
        ),
    )
    flat = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0 form-service-select",
            }
        ),
    )
