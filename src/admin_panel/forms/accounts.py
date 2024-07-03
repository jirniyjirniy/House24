# -*- coding: utf-8 -*-
import django.forms as forms
from django.contrib.auth import authenticate, get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.db import transaction

from src.admin_panel.models.accounts import Personal
from src.admin_panel.tasks import notification_password_changed

User = get_user_model()


class PersonalSignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Personal.ROLE_CHOICE, label="Роль")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": ""}), label="Email")
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "", "class": "password1"}),
        label="Пароль",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "", "class": "password2"}),
        label="Повторить Пароль",
    )
    phone = forms.CharField(
        max_length=19,
        label="Номер телефона",
        validators=[
            validators.MaxLengthValidator(19),
            validators.MinLengthValidator(19),
            validators.ProhibitNullCharactersValidator(),
            validators.RegexValidator(
                "^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$",
                message="Неверно введён номер телефона.",
            ),
        ],
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": ""}), label="Имя")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": ""}), label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
            "status",
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.is_staff = True
            user.save()
        Personal.objects.create(user=user, role=self.cleaned_data.get("role"))
        return user


class PersonalUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    role = forms.ChoiceField(choices=Personal.ROLE_CHOICE, label="Роль")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": ""}), label="Email")
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "", "class": "password1"}),
        label="Пароль",
        required=False,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "", "class": "password2"}),
        label="Повторить пароль",
        required=False,
    )
    phone = forms.CharField(
        max_length=19,
        label="Номер телефона",
        validators=[
            validators.RegexValidator(
                "^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$",
                message="Номер телефон ввёден не верно!",
            ),
            validators.MaxLengthValidator(19),
            validators.MinLengthValidator(19),
            validators.ProhibitNullCharactersValidator(),
        ],
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
        label="Имя",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
        label="Фамилия",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
            "status",
        )

    @transaction.atomic
    def save(self, commit=True):
        current_user = ""
        if self.request.user.is_authenticated:
            current_user = self.request.user
        user = super().save(commit=False)
        if commit:
            user.save()
        personal = Personal.objects.get(user=user)
        personal.role = self.cleaned_data["role"]
        personal.save()
        if self.cleaned_data.get("password1") == self.cleaned_data.get("password2"):
            if personal.user == current_user:
                user = authenticate(email=user.email, password=self.cleaned_data["password1"])
                if user:
                    login(self.request, user)
                    user.set_password(self.cleaned_data.get("password1"))
                    user.save()
                    update_session_auth_hash(self.request, user)
            else:
                personal.user.set_password(self.cleaned_data.get("password1"))
                personal.user.save()
                notification_password_changed.delay(personal.user.email)
        return user


class PersonalFilterForm(forms.Form):
    ROLE_CHOICE = (
        ("", ""),
        ("director", "Директор"),
        ("manager", "Управляющий"),
        ("accountant", "Бухгалтер"),
        ("electrician", "Электрик"),
        ("plumber", "Сантехник"),
        ("locksmith", "Слесарь"),
    )
    STATUS_CHOICE = (
        ("", ""),
        ("new", "Новый"),
        ("active", "Активен"),
        ("disabled", "Отключен"),
    )
    user = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
    role = forms.ChoiceField(
        label="",
        required=False,
        choices=ROLE_CHOICE,
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0",
            }
        ),
    )
    email = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
    phone = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control rounded-0"}),
    )
    status = forms.ChoiceField(
        label="",
        choices=STATUS_CHOICE,
        required=False,
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control select2-simple select2-success rounded-0",
            }
        ),
    )
