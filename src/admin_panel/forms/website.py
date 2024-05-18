# -*- coding: utf-8 -*-
import django.forms as forms

from ..models import AboutUs, AboutUsDocument, Contacts, InfoPhoto, MainPage, Photo, Seo, TariffSite


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = "__all__"
        exclude = ("gallery",)
        widgets = {"img": forms.FileInput(attrs={"class": ""})}


PhotoFormset = forms.modelformset_factory(Photo, form=PhotoForm, extra=0)
ExtraPhotoFormset = forms.modelformset_factory(Photo, form=PhotoForm, extra=0)
HousePhotoFormset = forms.modelformset_factory(model=Photo, form=PhotoForm, extra=5)


class InfoPhotoForm(forms.ModelForm):
    class Meta:
        model = InfoPhoto
        fields = "__all__"
        exclude = ("gallery",)
        widgets = {
            "img": forms.FileInput(attrs={"class": ""}),
            "description": forms.Textarea(attrs={"class": "summernote"}),
        }


InfoPhotoFormset = forms.modelformset_factory(model=InfoPhoto, form=InfoPhotoForm, extra=0, can_delete=True)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = "__all__"
        exclude = (
            "gallery",
            "seo",
        )
        widgets = {
            "show_app_links": forms.CheckboxInput(attrs={"class": "rounded-0 shadow-none"}),
            "description": forms.Textarea(attrs={"class": "summernote"}),
        }


class SeoForm(forms.ModelForm):
    class Meta:
        model = Seo
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": "6"}),
            "keywords": forms.Textarea(attrs={"rows": "6"}),
        }


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = "__all__"
        exclude = ("gallery", "seo", "extra_gallery")
        widgets = {
            "director_photo": forms.FileInput(attrs={"class": ""}),
            "description": forms.Textarea(attrs={"class": "summernote"}),
            "extra_description": forms.Textarea(attrs={"class": "summernote"}),
        }


class AboutUsDocumentForm(forms.ModelForm):
    class Meta:
        model = AboutUsDocument
        fields = "__all__"
        exclude = ("gallery",)
        widgets = {
            "img": forms.FileInput(attrs={"class": ""}),
        }


AboutUsDocumentFormset = forms.modelformset_factory(model=AboutUsDocument, form=AboutUsDocumentForm, extra=0)


class TariffSiteForm(forms.ModelForm):
    class Meta:
        model = TariffSite
        fields = "__all__"
        exclude = ("gallery", "seo")
        widgets = {
            "description": forms.Textarea(attrs={"class": "summernote"}),
        }


class InfoPhotoLiteForm(forms.ModelForm):
    img = forms.FileField(label="Файл")
    title = forms.FileField(label="Подпись")

    class Meta:
        model = InfoPhoto
        fields = "__all__"
        exclude = ("gallery", "description")
        widgets = {
            "img": forms.FileInput(attrs={"class": ""}),
        }


InfoPhotoLiteFormset = forms.modelformset_factory(model=InfoPhoto, form=InfoPhotoLiteForm, extra=0, can_delete=True)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = "__all__"
        exclude = ("seo",)
        widgets = {
            "description": forms.Textarea(attrs={"rows": "8", "class": "summernote"}),
            "coordinate": forms.Textarea(attrs={"rows": "6"}),
        }
