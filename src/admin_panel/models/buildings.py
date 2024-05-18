# -*- coding: utf-8 -*-
from django.db import models

from .accounts import *
from .website import *


class House(models.Model):
    title = models.CharField(verbose_name="Дом", max_length=100, default="", blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, default="", blank=True)
    gallery = models.ForeignKey("Gallery", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "house"
        app_label = "admin_panel"
        ordering = ["-id"]


class HouseUser(models.Model):
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey("Personal", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "house_user"


class Flat(models.Model):
    number = models.CharField(
        verbose_name="Номер квартиры",
        max_length=100,
    )
    square = models.DecimalField(
        verbose_name="Площадь (кв.м.)",
        max_digits=5,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    house = models.ForeignKey("House", verbose_name="Дом", on_delete=models.CASCADE, null=True)
    tariff = models.ForeignKey(
        "TariffSystem",
        verbose_name="Тариф",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    section = models.ForeignKey("Section", verbose_name="Секция", on_delete=models.CASCADE, null=True)
    floor = models.ForeignKey("Floor", verbose_name="Этаж", on_delete=models.CASCADE, null=True)
    flat_owner = models.ForeignKey(
        "FlatOwner",
        verbose_name="Владелец",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def application_label(self):
        return f"{self.number}, {self.house.title}"

    def __str__(self):
        return f"{self.number}"

    def delete(self, using=None, keep_parents=False):
        if hasattr(self, "personal_account"):
            pa = self.personal_account
            pa.section = None
            pa.house = None
            pa.save()
        super().delete()

    class Meta:
        db_table = "flat"


class Section(models.Model):
    title = models.CharField(verbose_name="Секция", max_length=100, default="", blank=True)
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "section"


class Floor(models.Model):
    title = models.CharField(verbose_name="Этаж", max_length=100, default="", blank=True)
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "floor"
