# -*- coding: utf-8 -*-
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView, ListView, View

from src.admin_panel.forms.house import FloorFormset, HouseFilterForm, HouseForm, HouseUserFormset, SectionFormset
from src.admin_panel.forms.website import HousePhotoFormset, PhotoFormset
from src.admin_panel.models import Floor, Gallery, House, HouseUser, Personal, Photo, Section

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
