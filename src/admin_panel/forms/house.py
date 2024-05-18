# -*- coding: utf-8 -*-
import django.forms as forms
from django.db.models import Q

from src.admin_panel.models import Flat, FlatOwner, Floor, House, HouseUser, Personal, PersonalAccount, Section


class HouseFilterForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control rounded-0", "placeholder": ""}),
    )
    address = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control rounded-0", "placeholder": ""}),
    )


class HouseForm(forms.ModelForm):
    title = forms.CharField(
        label="Название",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )
    address = forms.CharField(
        label="Адрес",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )

    class Meta:
        model = House
        fields = ("title", "address")


class HouseUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=Personal.objects.all(),
        label="ФИО",
        widget=forms.Select(attrs={"class": "form-role-select"}),
    )

    class Meta:
        model = HouseUser
        fields = ("user",)


HouseUserFormset = forms.modelformset_factory(model=HouseUser, form=HouseUserForm, can_delete=True, extra=0)


class SectionForm(forms.ModelForm):
    title = forms.CharField(
        label="Название",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )

    class Meta:
        model = Section
        fields = ("title",)


SectionFormset = forms.modelformset_factory(model=Section, form=SectionForm, can_delete=True, extra=0)


class FloorForm(forms.ModelForm):
    title = forms.CharField(
        label="Название",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )

    class Meta:
        model = Floor
        fields = ("title",)


FloorFormset = forms.modelformset_factory(model=Floor, form=FloorForm, extra=0, can_delete=True)


class FlatForm(forms.ModelForm):
    number = forms.CharField(
        label="Номер квартиры",
        widget=forms.TextInput(attrs={"class": "number", "placeholder": ""}),
    )
    square = forms.DecimalField(
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=False,
        label="Площадь",
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        label="Секция",
        required=False,
        widget=forms.Select(attrs={"class": "form-section-select"}),
    )
    floor = forms.ModelChoiceField(
        queryset=Floor.objects.all(),
        label="Этаж",
        required=False,
        widget=forms.Select(attrs={"class": "form-floor-select"}),
    )
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        label="Дом",
        required=False,
        widget=forms.Select(attrs={"class": "form-house-select"}),
    )
    personal_account_res = forms.CharField(
        widget=forms.TextInput(attrs={"class": "personal_account-res", "placeholder": ""}),
        required=False,
        label="Лицевой счет",
    )
    personal_account = forms.ModelChoiceField(
        queryset=PersonalAccount.objects.filter(flat__isnull=True),
        widget=forms.Select(attrs={"class": "personal_account-res"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(FlatForm, self).__init__(*args, **kwargs)

        self.fields["personal_account"].queryset = PersonalAccount.objects.filter(flat__isnull=True)

        self.fields["house"].empty_label = "Выберите..."
        self.fields["section"].empty_label = "Выберите..."
        self.fields["floor"].empty_label = "Выберите..."
        self.fields["flat_owner"].empty_label = "Выберите..."
        self.fields["tariff"].empty_label = "Выберите..."
        self.fields["personal_account"].empty_label = "или выберите из списка..."

        if self.instance.pk:
            if hasattr(self.instance, "personal_account"):
                self.fields["personal_account-res"].initial = self.instance.personal_account
                self.fields["personal_account"].queryset = PersonalAccount.objects.filter(
                    Q(flat__isnull=True) | Q(flat=self.instance.personal_account.flat)
                )
                self.fields["personal_account"].initial = self.instance.personal_account
            else:
                self.fields["personal_account"].queryset = PersonalAccount.objects.filter(Q(flat__isnull=True))

    def save(self, commit=True):
        instance = super(FlatForm, self).save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            if self.cleaned_data["personal_account_res"] == "":
                if hasattr(self.instance, "personal_account"):
                    pa = instance.personal_account
                    pa.flat = None
                    pa.section = None
                    pa.house = None
                    pa.save()
                    instance.personal_account = None
            else:
                if hasattr(self.instance, "personal_account"):
                    pa = instance.personal_account
                    pa.flat = None
                    pa.section = None
                    pa.house = None
                    pa.save()
                number = self.cleaned_data["persona_account-res"]
                pa, created = PersonalAccount.objects.get_or_create(number=number)
                pa.flat = instance
                pa.section = instance.section
                pa.house = instance.house
                pa.save()
        return instance

    class Meta:
        model = Flat
        fields = "__all__"
        widgets = {"number": forms.TextInput(attrs={"placeholder": ""})}


class FlatsFilterForm(forms.Form):
    DEBTS_CHOICE = (
        ("", ""),
        ("yes", "Есть долг"),
        ("no", "Нет долга"),
    )
    number = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
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
    floor = forms.ModelChoiceField(
        label="",
        required=False,
        queryset=Floor.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control select2-simple-floor select2-success rounded-0 form-floor-select"}
        ),
    )
    flat_owner = forms.ModelChoiceField(
        label="",
        required=False,
        queryset=FlatOwner.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2 select2-success rounded-0",
            }
        ),
    )
    have_debts = forms.ChoiceField(
        label="",
        required=False,
        choices=DEBTS_CHOICE,
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0",
            }
        ),
    )
