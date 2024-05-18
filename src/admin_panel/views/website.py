# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.views.generic import FormView, View

from ..forms.website import (
    AboutUsDocumentFormset,
    AboutUsForm,
    ContactForm,
    ExtraPhotoFormset,
    InfoPhotoFormset,
    MainPageForm,
    PhotoFormset,
    SeoForm,
    TariffSiteForm,
)
from ..models import AboutUsDocument, Contacts, Photo, SeviceSite, TariffSite
from ..models.business import AboutUs, MainPage, Seo


class MainPageView(FormView):
    def get(self, request, *args, **kwargs):
        main_page = MainPage.objects.prefetch_related("gallery__photo_set", "gallery__infophoto_set").first()
        seo_form = SeoForm(instance=Seo.objects.get(id=main_page.seo_id), prefix="seo")

        photo_formset = PhotoFormset(queryset=main_page.gallery.photo_set.all(), prefix="photo")
        info_photo_formset = InfoPhotoFormset(queryset=main_page.gallery.infophoto_set.all(), prefix="info_photo")
        main_form = MainPageForm(instance=main_page, prefix="main")
        context = {
            "main_form": main_form,
            "photo_formset": photo_formset,
            "info_photo_formset": info_photo_formset,
            "seo_form": seo_form,
        }
        return render(request, "manage_site/main_page.html", context=context)

    def post(self, request, *args, **kwargs):
        main_form = MainPageForm(
            request.POST,
            request.FILES,
            instance=MainPage.objects.first(),
            prefix="main",
        )
        seo = Seo.objects.get(id=MainPage.objects.first().seo_id)
        seo_form = SeoForm(request.POST, request.FILES, instance=seo, prefix="seo")
        photo_formset = PhotoFormset(request.POST, request.FILES, prefix="photo")
        info_photo_formset = InfoPhotoFormset(request.POST, request.FILES, prefix="info_photo")

        print("photo_formset", photo_formset.errors)
        print("info_photo_formset", info_photo_formset.errors)
        if main_form.is_valid() and photo_formset.is_valid() and info_photo_formset.is_valid() and seo_form.is_valid():
            main_form.save()
            photo_formset.save()
            info_photo_formset.save()
            seo_form.save()
        else:
            context = {
                "main_form": main_form,
                "photo_formset": photo_formset,
                "info_photo_formset": info_photo_formset,
                "seo_form": seo_form,
            }
            return render(request, "manage_site/main_page.html", context)
        return redirect("main_page_update")


class AboutUsView(FormView):
    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.prefetch_related("gallery__photo_set", "extra_gallery__photo_set").first()
        seo_form = SeoForm(instance=Seo.objects.get(id=about_us.seo_id), prefix="seo")
        photo_formset = ExtraPhotoFormset(queryset=about_us.gallery.photo_set.all(), prefix="photo")
        extra_photo_formset = ExtraPhotoFormset(queryset=about_us.extra_gallery.photo_set.all(), prefix="extra_photo")
        about_us_form = AboutUsForm(instance=about_us, prefix="about")
        docs_formset = AboutUsDocumentFormset(prefix="docs")

        data = {
            "about_us_form": about_us_form,
            "photo_formset": photo_formset,
            "extra_photo_formset": extra_photo_formset,
            "docs_formset": docs_formset,
            "seo_form": seo_form,
        }
        return render(request, "manage_site/about_us.html", context=data)

    def post(self, request, *args, **kwargs):
        about_us = AboutUs.objects.first()
        about_us_form = AboutUsForm(request.POST, request.FILES, instance=about_us, prefix="about")
        seo = Seo.objects.get(id=about_us.seo_id)
        docs_formset = AboutUsDocumentFormset(request.POST, request.FILES, prefix="docs")
        seo_form = SeoForm(request.POST, request.FILES, instance=seo, prefix="seo")
        photo_formset = ExtraPhotoFormset(request.POST, request.FILES, prefix="photo")
        extra_photo_formset = ExtraPhotoFormset(request.POST, request.FILES, prefix="extra_photo")
        if (
            about_us_form.is_valid()
            and photo_formset.is_valid()
            and extra_photo_formset.is_valid()
            and seo_form.is_valid()
            and docs_formset.is_valid()
        ):
            about_us_form.save()
            seo_form.save()
            docs_formset.save()
            instances = photo_formset.save(commit=False)
            for instance in instances:
                instance.gallery_id = about_us.gallery.id
                instance.save()
            extra_instances = extra_photo_formset.save(commit=False)
            for instance in extra_instances:
                instance.gallery_id = about_us.extra_gallery.id
                instance.save()
        else:
            data = {
                "about_us_form": about_us_form,
                "photo_formset": photo_formset,
                "extra_photo_formset": extra_photo_formset,
                "seo_form": seo_form,
                "docs_formset": docs_formset,
            }
            return render(request, "manage_site/about_us.html", context=data)
        return redirect("about_us")


class DeletePhotoView(View):
    def get(self, request, pk, *args, **kwargs):
        obj = Photo.objects.get(pk=pk)
        obj.delete()
        return redirect("about_us")


class DeleteDocsView(View):
    def get(self, request, pk, *args, **kwargs):
        obj = AboutUsDocument.objects.get(pk=pk)
        obj.delete()
        return redirect("about_us")


class SiteServicesView(FormView):
    def get(self, request, *args, **kwargs):
        service_site = SeviceSite.objects.prefetch_related("gallery__infophoto_set").first()
        seo_form = SeoForm(instance=Seo.objects.get(id=service_site.seo_id), prefix="seo")
        info_photo_formset = InfoPhotoFormset(queryset=service_site.gallery.infophoto_set.all(), prefix="info_photo")

        context = {
            "seo_form": seo_form,
            "info_photo_formset": info_photo_formset,
        }
        return render(request, "manage_site/site_service.html", context)

    def post(self, request, *args, **kwargs):
        seo_form = SeoForm(
            request.POST,
            instance=Seo.objects.get(id=SeviceSite.objects.first().seo_id),
            prefix="seo",
        )
        info_photo_formset = InfoPhotoFormset(request.POST, request.FILES, prefix="info_photo")
        service_site = SeviceSite.objects.first()

        if seo_form.is_valid() and info_photo_formset.is_valid():
            instances = info_photo_formset.save(commit=False)
            for instance in instances:
                instance.gallery_id = service_site.gallery.id
                instance.save()
            for obj in info_photo_formset.deleted_objects:
                obj.delete()
            seo_form.save()
        else:
            context = {
                "seo_form": seo_form,
                "info_photo_formset": info_photo_formset,
            }
            return render(request, "manage_site/site_service.html", context)
        return redirect("services_page")


class TariffSiteView(FormView):
    def get(self, request, *args, **kwargs):
        tariff = TariffSite.objects.prefetch_related("gallery__infophoto_set").first()
        tariff_site_form = TariffSiteForm(instance=tariff, prefix="info_photo")
        seo_form = SeoForm(instance=Seo.objects.get(id=tariff.seo_id), prefix="seo")
        info_photo_formset = InfoPhotoFormset(queryset=tariff.gallery.infophoto_set.all(), prefix="info_photo")
        context = {
            "seo_form": seo_form,
            "info_photo_formset": info_photo_formset,
            "tariff_site_form": tariff_site_form,
        }
        return render(request, "manage_site/site_tariff.html", context)

    def post(self, request, *args, **kwargs):
        tariff = TariffSite.objects.first()
        tariff_site_form = TariffSiteForm(request.POST, request.FILES, prefix="info_photo")
        info_photo_formset = InfoPhotoFormset(request.POST, request.FILES, prefix="info_photo")
        seo_form = SeoForm(
            request.POST,
            request.FILES,
            instance=Seo.objects.get(id=TariffSite.objects.first().seo_id),
            prefix="seo",
        )

        if tariff_site_form.is_valid() and info_photo_formset.is_valid() and seo_form.is_valid():
            instances = info_photo_formset.save(commit=False)
            for instance in instances:
                instance.gallery_id = tariff.gallery.id
                instance.save()
            for obj in info_photo_formset.deleted_objects:
                obj.delete()
            tariff_site_form.save()
            seo_form.save()
        else:
            context = {
                "seo_form": seo_form,
                "info_photo_formset": info_photo_formset,
                "tariff_site_form": tariff_site_form,
            }
            return render(request, "manage_site/site_tariff.html", context)
        return redirect("tariffs_page")


class ContactSiteView(FormView):
    def get(self, request, *args, **kwargs):
        contacts = Contacts.objects.first()
        contacts_form = ContactForm(instance=contacts, prefix="contact")
        seo_form = SeoForm(instance=Seo.objects.get(id=contacts.seo_id), prefix="seo")

        data = {
            "contacts_form": contacts_form,
            "seo_form": seo_form,
        }
        return render(request, "manage_site/site_contact.html", context=data)

    def post(self, request, *args, **kwargs):
        contacts_form = ContactForm(request.POST, instance=Contacts.objects.first(), prefix="contact")
        seo_form = SeoForm(
            request.POST,
            instance=Seo.objects.get(id=Contacts.objects.first().seo_id),
            prefix="seo",
        )
        if contacts_form.is_valid() and seo_form.is_valid():
            contacts_form.save()
            seo_form.save()
        else:
            data = {
                "contacts_form": contacts_form,
                "seo_form": seo_form,
            }
            return render(request, "manage_site/site_contact.html", context=data)
        return redirect("contacts_page")
