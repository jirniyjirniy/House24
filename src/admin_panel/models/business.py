# -*- coding: utf-8 -*-
from django.db import models

from .accounts import *
from .buildings import *
from .website import *


class TariffSystem(models.Model):
    title = models.CharField(verbose_name="Название тарифа", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Описание тарифа", default="", blank=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "tariff_system"
        ordering = ["-date_edited"]


class TariffService(models.Model):
    price = models.DecimalField(verbose_name="Цена", default=0, max_digits=10, decimal_places=2)
    currency = models.CharField(verbose_name="Валюта", blank=True, default="грн", max_length=10)
    tariff = models.ForeignKey("TariffSystem", on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey("Service", verbose_name="Услуга", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "tariff_service"


class Service(models.Model):
    title = models.CharField(verbose_name="Услуга", max_length=100, default="", blank=True)
    show_in_indication = models.BooleanField(default=False, verbose_name="Показывать в счетчиках")
    measure = models.ForeignKey(
        "Measure",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Ед. изм.",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "service"


class Measure(models.Model):
    title = models.CharField(verbose_name="Ед. изм.", max_length=100, default="", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "measure"


class PaymentDetail(models.Model):
    title = models.CharField(verbose_name="Название компании", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Информация", default="", blank=True)

    class Meta:
        db_table = "payment_detail"


class Article(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100, default="", blank=True)
    PLUS_MINUS = (
        ("plus", "Приход"),
        ("minus", "Расход"),
    )
    debit_credit = models.CharField(
        verbose_name="Приход/расход",
        choices=PLUS_MINUS,
        max_length=100,
        default="plus",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "article"


class PersonalAccount(models.Model):
    number = models.CharField(verbose_name="№", max_length=100, unique=True, default="", blank=True)
    STATUS_CHOICE = (
        ("active", "Активен"),
        ("disabled", "Не активен"),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="active", verbose_name="Статус")
    section = models.ForeignKey(
        "Section",
        verbose_name="Секция",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    house = models.ForeignKey("House", verbose_name="Дом", on_delete=models.SET_NULL, null=True, blank=True)
    flat = models.OneToOneField(
        "Flat",
        verbose_name="Квартира",
        on_delete=models.SET_NULL,
        related_name="personal_account",
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=20,
    )

    def __str__(self):
        return self.number

    class Meta:
        db_table = "personal_account"
        ordering = ["-id"]


class Paybox(models.Model):
    PLUS_MINUS = (
        ("plus", "Приход"),
        ("minus", "Расход"),
    )
    number = models.CharField(verbose_name="", max_length=100, default="", blank=True)
    comment = models.TextField(verbose_name="Комментарий", default="", blank=True)
    date_published = models.DateField()
    total = models.DecimalField(verbose_name="Сумма", decimal_places=2, max_digits=20)
    flat_owner = models.ForeignKey("FlatOwner", on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("Personal", on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(
        default=True,
    )
    personal_account = models.ForeignKey("PersonalAccount", on_delete=models.SET_NULL, null=True, blank=True)
    debit_credit = models.CharField(
        verbose_name="Приход/расход",
        choices=PLUS_MINUS,
        max_length=100,
        default="plus",
    )

    class Meta:
        db_table = "paybox"
        ordering = ["-date_published"]


class Receipt(models.Model):
    number = models.CharField(verbose_name="", max_length=100, default="", blank=True)
    is_complete = models.BooleanField(
        default=True,
    )
    date_published = models.DateField(default="2012-12-12")
    STATUS_CHOICE = (
        ("paid", "Оплачена"),
        ("partially_paid", "Частично оплачена"),
        ("unpaid", "Не оплачена"),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="unpaid", verbose_name="Статус")
    start_date = models.DateField(default="2012-12-12")
    end_date = models.DateField(default="2012-12-12")
    service = models.ManyToManyField("Service", blank=True)
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE)
    tariff = models.ForeignKey("TariffSystem", on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(default=0, blank=True, decimal_places=2, max_digits=20)

    class Meta:
        db_table = "receipt"
        ordering = ["-date_published"]


class ReceiptExcelDoc(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100, default="", blank=True)
    file = models.FileField(
        upload_to="receipt",
        verbose_name="Загрузить пользовательский шаблон",
    )
    by_default = models.BooleanField(default=False)

    class Meta:
        db_table = "receipt_excel_doc"


class ReceiptService(models.Model):
    unit_price = models.DecimalField(verbose_name="Цена", default=0.0, max_digits=10, decimal_places=2)
    consumption = models.DecimalField(verbose_name="Цена", default=0.0, max_digits=15, decimal_places=2)
    receipt = models.ForeignKey("Receipt", on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        "Service",
        verbose_name="Услуга",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    measure = models.ForeignKey(
        "Measure",
        verbose_name="Ед. изм.",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def calc_sum(self):
        return round(self.consumption * self.unit_price, 2)

    class Meta:
        db_table = "receipt-service"


class Indication(models.Model):
    number = models.CharField(verbose_name="", max_length=100, default="", blank=True)
    indication_val = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name="Показания",
        default=0.0,
        blank=True,
    )
    date_published = models.DateField()
    STATUS_CHOICE = (
        ("new", "Новое"),
        ("considered", "Учтено"),
        ("considered and paid", "Учтено и оплачено"),
        ("null", "Нулевое"),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="new", verbose_name="Статус")
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Счётчик",
    )
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, verbose_name="Квартира")

    class Meta:
        db_table = "indication"
        ordering = ["-date_published"]


class Application(models.Model):
    date_published = models.DateField()
    comment = models.TextField(verbose_name="Комментарий", default="", blank=True)
    description = models.TextField(verbose_name="Описание", default="", blank=True)
    time_published = models.TimeField()
    STATUS_CHOICE = (
        ("", "Выберите..."),
        ("new", "Новое"),
        ("in work", "В работе"),
        ("complete", "Выполнено"),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="new", verbose_name="Статус")
    user = models.ForeignKey("Personal", on_delete=models.SET_NULL, null=True)
    ROLE_CHOICE = (
        ("", "Любой специалист"),
        ("director", "Директор"),
        ("manager", "Управляющий"),
        ("accountant", "Бухгалтер"),
        ("electrician", "Электрик"),
        ("plumber", "Сантехник"),
    )
    user_type = models.CharField(choices=ROLE_CHOICE, max_length=100, default="")
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, verbose_name="Квартира")

    class Meta:
        db_table = "application"
        ordering = ["-date_published"]


class MailBox(models.Model):
    title = models.CharField(max_length=100, verbose_name="", default="", blank=True)
    description = models.TextField(default="", verbose_name="", blank=True)
    date_published = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey("Personal", on_delete=models.CASCADE, null=True)
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True, blank=True)
    floor = models.ForeignKey("Floor", on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey("Section", on_delete=models.CASCADE, null=True, blank=True)
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, null=True, blank=True)
    flat_owners = models.ManyToManyField("FlatOwner")
    unread = models.BooleanField(default=True)

    class Meta:
        db_table = "mailbox"
