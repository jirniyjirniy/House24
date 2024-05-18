# -*- coding: utf-8 -*-
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from src.admin_panel.forms.house import FlatForm, FlatsFilterForm
from src.admin_panel.models import Flat


class FlatListView(ListView):
    template_name = "flat/flats.html"
    context_object_name = "flats"
    queryset = Flat.objects.all()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FlatsFilterForm()
        return context


class FlatFilteredListView(ListView):
    template_name = "flat/flats.html"
    context_object_name = "flats"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FlatsFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        flats = Flat.objects.all()
        form_filter = FlatsFilterForm(self.request.GET)
        qs = []

        if form_filter.is_valid():
            if form_filter.cleaned_data["number"]:
                qs.append(Q(number=form_filter.cleaned_data["number"]))
            if form_filter.cleaned_data["house"]:
                qs.append(Q(house_id=form_filter.cleaned_data["house"].id))
            if form_filter.cleaned_data["section"]:
                qs.append(Q(section_id=form_filter.cleaned_data["section"].id))
            if form_filter.cleaned_data["floor"]:
                qs.append(Q(floor_id=form_filter.cleaned_data["floor"].id))
            if form_filter.cleaned_data["flat_owner"]:
                full_name = str(form_filter.cleaned_data["flat_owner"]).split()
                qs.append(
                    Q(
                        Q(flat_owner__patronymic__icontains=full_name[0])
                        | Q(flat_owner__user__first_name__icontains=full_name[1])
                        | Q(flat_owner__user__last_name__icontains=full_name[2])
                    )
                )
            if form_filter.cleaned_data["have_debts"]:
                if form_filter.cleaned_data["have_debts"] == "no":
                    qs.append(Q(personal_account__balance__gte=0))
                elif form_filter.cleaned_data["have_debts"] == "yes":
                    qs.append(Q(personal_account__balance__lt=0))
            q = Q()

            for obj in qs:
                q = q & obj
            flats = Flat.objects.filter(q)
        return flats


class FlatCreateView(CreateView):
    model = Flat
    template_name = "flat/flat_form.html"
    form_class = FlatForm
    success_url = reverse_lazy("flats")


class FlatDetailView(DetailView):
    model = Flat
    template_name = "flat/flat_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flat = Flat.objects.get(pk=self.kwargs["pk"])
        context["flat"] = flat
        return context


class FlatUpdateView(UpdateView):
    model = Flat
    template_name = "flat/flat_form.html"
    form_class = FlatForm
    success_url = reverse_lazy("flats")


class FlatDeleteView(DeleteView):
    queryset = Flat.objects.all()
    success_url = reverse_lazy("flats")
