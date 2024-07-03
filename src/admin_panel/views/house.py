# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView, ListView, View

from src.admin_panel.forms.house import FloorFormset, HouseFilterForm, HouseForm, HouseUserFormset, SectionFormset
from src.admin_panel.forms.website import HousePhotoFormset, PhotoFormset
from src.admin_panel.models import Floor, Gallery, House, HouseUser, Personal, Photo, Section, Flat, PersonalAccount, \
    FlatOwner, CustomUser, TariffSystem, Service, Indication

from .other import StaffRequiredMixin


class HouseListView(StaffRequiredMixin, ListView):
    template_name = "house/houses.html"
    context_object_name = "houses"
    queryset = House.objects.all()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = HouseFilterForm()
        return context


class HouseFilteredListView(StaffRequiredMixin, ListView):
    template_name = "house/houses.html"
    context_object_name = "houses"
    paginate_by = 20

    def get_context_data(self, obj_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = HouseFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        houses = House.objects.all()
        form_filter = HouseFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["title"]:
                qs.append(Q(title__icontains=form_filter.cleaned_data["title"]))
            if form_filter.cleaned_data["address"]:
                qs.append(Q(address__icontains=form_filter.cleaned_data["address"]))
            q = Q()
            for item in qs:
                q = q & item
            houses = houses.filter(q)
        return houses


class HouseDetailView(StaffRequiredMixin, DetailView):
    model = House
    template_name = "house/house_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = House.objects.prefetch_related("gallery__photo_set", "houseuser_set").get(pk=self.kwargs["pk"])
        photos = house.gallery.photo_set.all()
        users = house.houseuser_set.all()
        context["house"] = house
        context["photos"] = photos
        context["users"] = users
        return context


class CreateHouseView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        house_form = HouseForm()
        personals = Personal.objects.all()
        photo_formset = HousePhotoFormset(queryset=Photo.objects.none(), prefix="gallery")
        section_formset = SectionFormset(queryset=Section.objects.none(), prefix="section")
        floor_formset = FloorFormset(queryset=Floor.objects.none(), prefix="floor")
        house_user_formset = HouseUserFormset(queryset=HouseUser.objects.none(), prefix="personal")

        context = {
            "house_form": house_form,
            "personals": personals,
            "photo_formset": photo_formset,
            "section_formset": section_formset,
            "floor_formset": floor_formset,
            "house_user_formset": house_user_formset,
        }
        return render(request, "house/house_form.html", context)

    def post(self, request, *args, **kwargs):
        house_form = HouseForm(request.POST, request.FILES)
        section_formset = SectionFormset(request.POST, request.FILES, prefix="section")
        floor_formset = FloorFormset(request.POST, request.FILES, prefix="floor")
        photo_formset = HousePhotoFormset(request.POST, request.FILES, prefix="gallery")
        house_user_formset = HouseUserFormset(request.POST, request.FILES, prefix="personal")

        if (
                section_formset.is_valid()
                and floor_formset.is_valid()
                and photo_formset.is_valid()
                and house_user_formset.is_valid()
                and house_form.is_valid()
        ):
            house_obj = house_form.save()
            house_user_instance = house_user_formset.save(commit=False)
            for instance in house_user_instance:
                instance.house_id = house_obj.id
                instance.save()
            gallery = Gallery.objects.create()
            house_obj.gallery_id = gallery.id
            for photo_form in photo_formset:
                instance = photo_form.save(commit=False)
                instance.gallery_id = gallery.id
                instance.save()
            section_instances = section_formset.save(commit=False)
            floor_instances = floor_formset.save(commit=False)
            for instance in section_instances:
                instance.house_id = house_obj.id
                instance.save()

            for instance in floor_instances:
                instance.house_id = house_obj.id
                instance.save()
            house_obj.save()

        else:
            context = {
                "house_form": house_form,
                "section_formset": section_formset,
                "floor_formset": floor_formset,
                "house_user_formset": house_user_formset,
                "photo_formset": photo_formset,
            }
            return render(request, "house/house_form.html", context)
        return redirect("houses")


class UpdateHouseView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        personals = Personal.objects.all()
        house = House.objects.get(pk=pk)
        house_form = HouseForm(instance=house)
        photo_formset = PhotoFormset(queryset=Photo.objects.filter(gallery_id=house.gallery_id), prefix="gallery")
        section_formset = SectionFormset(queryset=Section.objects.filter(house=house), prefix="section")
        floor_formset = FloorFormset(queryset=Floor.objects.filter(house=house), prefix="floor")
        house_user_formset = HouseUserFormset(queryset=HouseUser.objects.filter(house_id=house.id), prefix="personal")
        data = {
            "house_form": house_form,
            "personals": personals,
            "house": house,
            "photo_formset": photo_formset,
            "section_formset": section_formset,
            "floor_formset": floor_formset,
            "house_user_formset": house_user_formset,
        }
        return render(request, "house/house_update.html", context=data)

    def post(self, request, pk, *args, **kwargs):
        house = House.objects.get(pk=pk)
        house_form = HouseForm(request.POST, request.FILES, instance=house)
        section_formset = SectionFormset(request.POST, request.FILES, prefix="section")
        floor_formset = FloorFormset(request.POST, request.FILES, prefix="floor")
        photo_formset = PhotoFormset(request.POST, request.FILES, prefix="gallery")
        house_user_formset = HouseUserFormset(request.POST, request.FILES, prefix="personal")

        if (
                section_formset.is_valid()
                and floor_formset.is_valid()
                and house_form.is_valid()
                and photo_formset.is_valid()
                and house_user_formset.is_valid()
        ):
            house_obj = house_form.save()
            house_user_instances = house_user_formset.save(commit=False)
            for instance in house_user_instances:
                instance.house_id = house_obj.id
                instance.save()
            photo_instances = photo_formset.save(commit=False)
            gallery = Gallery.objects.get(house=house)
            for photo_instance in photo_instances:
                photo_instance.gallery_id = gallery.id
                photo_instance.save()

            section_instances = section_formset.save(commit=False)
            floor_instances = floor_formset.save(commit=False)
            for instance in section_instances:
                instance.house_id = house_obj.id
                instance.save()
            for instance in floor_instances:
                instance.house_id = house_obj.id
                instance.save()
            house_obj.save()

            for obj in section_formset.deleted_objects:
                obj.delete()

            for obj in floor_formset.deleted_objects:
                obj.delete()

            for obj in house_user_formset.deleted_objects:
                obj.delete()

        else:
            data = {
                "house_form": house_form,
                "section_formset": section_formset,
                "floor_formset": floor_formset,
                "photo_formset": photo_formset,
                "house_user_formset": house_user_formset,
            }
            return render(request, "house/house_update.html", context=data)
        return redirect("houses")


class DeleteHouseView(StaffRequiredMixin, FormView):
    def post(self, request, pk, *args, **kwargs):
        house = House.objects.get(pk=pk)
        gallery = Gallery.objects.get(pk=house.gallery_id)
        house.delete()
        gallery.delete()
        return redirect("houses")


class GetHouseInfoView(View):
    def get(self, request, pk, *args, **kwargs):
        house = House.objects.prefetch_related("section_set", "floor_set", "flat_set").get(pk=pk)
        sections = serializers.serialize("json", house.section_set.all())
        floor = serializers.serialize("json", house.floor_set.all())
        flat = serializers.serialize("json", house.flat_set.all())
        house = serializers.serialize("json", [house])
        context = {
            "house": house,
            "sections": sections,
            "floors": floor,
            "flat": flat,
        }
        return JsonResponse(context, safe=False)


class GetSectionInfoView(View):
    def get(self, request, pk, *args, **kwargs):
        section = Section.objects.prefetch_related("flat_set").get(pk=pk)
        flats = serializers.serialize("json", section.flat_set.all())
        context = {
            'flats': flats,
        }
        return JsonResponse(context, safe=False)


class GetAllFlatsView(View):
    def get(self, request):
        flats = Flat.objects.all()
        flats = serializers.serialize("json", flats)
        all_personal_accounts = PersonalAccount.objects.all()
        all_personal_accounts = serializers.serialize("json", all_personal_accounts)

        context = {
            "flats": flats,
            "all_personal_accounts": all_personal_accounts,
        }
        return JsonResponse(context, safe=False)


class GetFlatOwnerView(View):
    def get(self, request, pk):
        flat_owner = FlatOwner.objects.prefetch_related('flat_set').get(pk=pk)
        flats = flat_owner.flat_set.select_related('house').all()
        personal_accounts = PersonalAccount.objects.filter(flat__in=flats.values_list('id', flat=True))
        flats = serializers.serialize("json", flats)
        personal_accounts = serializers.serialize("json", personal_accounts)
        context = {
            "flats": flats,
            "personal_account": personal_accounts,
        }
        return JsonResponse(context, safe=False)


class GetFlatsForMail(View):
    def get(self, request, section_id, floor_id):
        flats = Flat.objects.all()
        if self.kwargs['section_id'] != None:
            flats = flats.filter(section__id=self.kwargs['section_id'])
        if self.kwargs['floor_id'] != None:
            flats = flats.filter(floor__id=self.kwargs['floor_id'])

        flats = serializers.serialize("json", flats)
        context = {
            "flats": flats,
        }
        return JsonResponse(context, safe=False)


class GetFlatInfoView(StaffRequiredMixin, View):
    def get(self, request, pk):
        data = {}
        flat = Flat.objects.get(pk=pk)
        try:
            flat_owner_obj = FlatOwner.objects.get(flat=flat)
            flat_owner = serializers.serialize('json', [flat_owner_obj])
            data['flat_owner'] = flat_owner
            user = CustomUser.objects.get(client=flat_owner_obj)
            user = serializers.serialize('json', [user])
            data['user'] = user
        except ObjectDoesNotExist:
            pass
        try:
            if flat.personal_account is not None:
                personal_account = flat.personal_account
                personal_account = serializers.serialize('json', [personal_account])
                data['personal_account'] = personal_account
        except ObjectDoesNotExist:
            pass
        try:
            if flat.tariff is not None:
                tariff = TariffSystem.objects.get(pk=flat.tariff.pk)
                tariff = serializers.serialize('json', [tariff])
                data['tariff'] = tariff
        except ObjectDoesNotExist:
            pass
        return JsonResponse(data, safe=False)


class GetTariffInfoView(StaffRequiredMixin, View):
    def get(self, request, pk):
        tariff = TariffSystem.objects.prefetch_related('tariffservice_set').get(pk=pk)
        tariff_service = serializers.serialize('json', tariff.tariffservice_set.all())
        context = {
            "tariff_services": tariff_service,
        }
        return JsonResponse(context, safe=False)


class GetServiceInfoView(StaffRequiredMixin, View):
    def get(self, request, pk):
        service = Service.objects.get(pk=pk)
        service = serializers.serialize('json', [service])
        context = {
            "service": service,
        }
        return JsonResponse(context, safe=False)


class GetIndicationInfoView(StaffRequiredMixin, View):
    def get(self, request, flat_id, service_id):
        indication = Indication.objects.filter(flat_id=flat_id, service_id=service_id)
        if indication.count() != 0:
            indication = serializers.serialize('json', indication)
            context = {
                "indication": indication,
            }
        else:
            return JsonResponse({}, safe=False)
        return JsonResponse(context, safe=False)
