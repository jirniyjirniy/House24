# -*- coding: utf-8 -*-
import os

from django.core import validators
from django.db import models

from src.admin_panel.utilities import get_timestamp_path


class Gallery(models.Model):
    title = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "gallery"


class Photo(models.Model):
    img = models.ImageField(upload_to=get_timestamp_path, verbose_name="", null=True, blank=True)
    gallery = models.ForeignKey("Gallery", on_delete=models.SET_NULL, null=True, related_name="photo_set")

    class Meta:
        db_table = "photo"


class InfoPhoto(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Описание", default="", blank=True)
    img = models.ImageField(upload_to=get_timestamp_path, verbose_name="", null=True, blank=True)
    gallery = models.ForeignKey("Gallery", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "info_photo"


class Seo(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Описание", default="", blank=True)
    keywords = models.TextField(verbose_name="Ключевые слова", default="", blank=True)

    class Meta:
        db_table = "seo"


class AboutUs(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Краткий текст", default="", blank=True)
    extra_title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    extra_description = models.TextField(verbose_name="Краткий текст", default="", blank=True)
    director_photo = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name="Рекомендуемый размер: (250x310)",
        null=True,
        blank=True,
    )
    gallery = models.ForeignKey(
        "Gallery",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_query_name="gallery_about",
    )
    extra_gallery = models.ForeignKey(
        "Gallery",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="extra_gallery_about",
    )
    seo = models.OneToOneField("Seo", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "about_us"


class AboutUsDocument(models.Model):
    file = models.FileField(
        upload_to="docs",
        verbose_name="PDF, JPG (макс. размер 20 Mb)",
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name="Название документа", max_length=100, default="", blank=True)
    about_us = models.ForeignKey("AboutUs", on_delete=models.SET_NULL, null=True, blank=True)

    def get_extension(self):
        ext = os.path.splitext(self.file.name)[1]
        return ext.lower()

    class Meta:
        db_table = "about_us_document"


class MainPage(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Краткий текст", default="", blank=True)
    gallery = models.ForeignKey(
        "Gallery",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_query_name="gallery_main",
    )
    seo = models.OneToOneField("Seo", on_delete=models.CASCADE, null=True)
    show_app_links = models.BooleanField(verbose_name=" Показать ссылки на приложения", default=True)

    class Meta:
        db_table = "main_page"


class SeviceSite(models.Model):
    gallery = models.ForeignKey(
        "Gallery",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_query_name="gallery_service",
    )
    seo = models.OneToOneField("Seo", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "service_site"


class TariffSite(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Краткий текст", default="", blank=True)
    gallery = models.ForeignKey(
        "Gallery",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_query_name="gallery_tariff",
    )

    seo = models.OneToOneField("Seo", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "tarif_site"


class Contacts(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default="", blank=True)
    description = models.TextField(verbose_name="Краткий текст", default="", blank=True)
    full_name = models.CharField(verbose_name="ФИО", max_length=100, default="", blank=True)
    location = models.CharField(verbose_name="Локация", max_length=100, default="", blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, default="", blank=True)
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="E-mail",
        null=True,
        blank=True,
        validators=[
            validators.EmailValidator(),
        ],
    )
    phone = models.CharField(
        max_length=19,
        verbose_name="Телефон",
        validators=[
            validators.MaxLengthValidator(19),
            validators.MinLengthValidator(19),
            validators.ProhibitNullCharactersValidator(),
            validators.RegexValidator(
                "^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$",
                message="Неверно введён номер телефона.Пример ввода: +38 (093) 123-12-34",
            ),
        ],
    )
    site_link = models.URLField(
        verbose_name="Ссылка на коммерческий сайт",
        default="",
        validators=[
            validators.URLValidator(
                regex="https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)",
                message="XYZ",
            ),
        ],
    )
    coordinate = models.TextField(verbose_name="Код карты")
    seo = models.OneToOneField("Seo", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "contacts"
