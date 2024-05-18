# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from src.admin_panel.forms.indications import CounterIndicationsFilterForm, IndicationForm, IndicationsFilterForm
from src.admin_panel.models import Flat, Indication, Service

from .other import StaffRequiredMixin


class IndicationsList(StaffRequiredMixin, ListView):
    template_name = "indication/indications.html"
    context_object_name = "indications"
    queryset = Indication.objects.order_by("flat", "service", "-date_published").distinct("flat", "service")
    paginate_by = 10

    def get_context_data(self, obj_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = IndicationsFilterForm()
        return context


class IndicationsFilteredList(StaffRequiredMixin, ListView):
    template_name = "indication/indications.html"
    context_object_name = "indications"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = IndicationsFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        indications = Indication.objects.order_by("flat", "service", "-date_published").distinct("flat", "service")
        form_filter = IndicationsFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["flat"]:
                qs.append(Q(flat__number=form_filter.cleaned_data["flat"]))
            if form_filter.cleaned_data["house"]:
                qs.append(Q(flat__house_id=form_filter.cleaned_data["house"].id))
            if form_filter.cleaned_data["section"]:
                qs.append(Q(flat__section_id=form_filter.cleaned_data["section"].id))
            if form_filter.cleaned_data["service"]:
                qs.append(Q(service_id=form_filter.cleaned_data["service"].id))
            q = Q()
            for item in qs:
                q = q & item
            indications = (
                Indication.objects.order_by("flat", "service", "-date_published").distinct("flat", "service").filter(q)
            )
        return indications


class CounterIndicationsFilteredList(StaffRequiredMixin, ListView):
    template_name = "indication/indications.html"
    context_object_name = "indication"
    paginate_by = 20

    def get_context_data(self, obj_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flat"] = Flat.objects.get(pk=self.kwargs["flat"])
        context["filter_form"] = CounterIndicationsFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        indications = Indication.objects.filter(flat_id=self.kwargs["flat"])
        form_filter = CounterIndicationsFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["house"]:
                qs.append(Q(flat__house_id=form_filter.cleaned_data["house"].id))
            if form_filter.cleaned_data["section"]:
                qs.append(Q(flat__section_id=form_filter.cleaned_data["section"].id))
            if form_filter.cleaned_data["service"]:
                qs.append(Q(service_id=form_filter.cleaned_data["service"].id))
            if form_filter.cleaned_data["number"]:
                qs.append(Q(number__icontains=form_filter.cleaned_data["number"]))
            if form_filter.cleaned_data["daterange"]:
                date_start, date_end = str(form_filter.cleaned_data["daterange"]).split("-")
                date_start = date_start.split("/")
                date_end = date_end.split("/")
                date_start.reverse()
                date_end.reverse()
                date_start = "-".join(date_start)
                date_end = "-".join(date_end)
                qs.append(Q(Q(date_published__gte=date_start) & Q(date_published__lte=date_end)))
            if form_filter.cleaned_data["status"]:
                qs.append(Q(status=form_filter.cleaned_data["status"]))
            q = Q()
            for item in qs:
                q = q & item
            indications = Indication.objects.filter(flat_id=self.kwargs["flat"]).filter(q)
        return indications


class CounterIndicationsList(StaffRequiredMixin, ListView):
    template_name = "indication/counter_indications_list.html"
    context_object_name = "indications"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flat"] = Flat.objects.get(pk=self.kwargs["flat"])
        context["filter_form"] = CounterIndicationsFilterForm(initial={"service": self.kwargs["service"]})
        context["service"] = Service.objects.get(pk=self.kwargs["service"])
        return context

    def get_queryset(self):
        queryset = Indication.objects.filter(flat_id=self.kwargs["flat"], service_id=self.kwargs["service"])
        return queryset


class FlatIndicationsList(StaffRequiredMixin, ListView):
    template_name = "indication/counter_indications_list.html"
    context_object_name = "indication"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flat = Flat.objects.get(pk=self.kwargs["flat"])
        context["flat"] = flat
        context["filter_form"] = CounterIndicationsFilterForm(initial=flat.number)
        return context

    def get_queryset(self):
        queryset = Indication.objects.filter(flat_id=self.kwargs["flat"])
        return queryset


class IndicationDetail(StaffRequiredMixin, DetailView):
    model = Indication
    template_name = "indication/indication_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indications = Indication.objects.get(pk=self.kwargs["pk"])
        context["indication"] = indications
        return context


class CreateIndication(StaffRequiredMixin, CreateView):
    model = Indication
    template_name = "indication/indication_form.html"
    form_class = IndicationForm
    success_url = reverse_lazy("indicators")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crate_new_indication"] = False
        return context

    def post(self, request, *args, **kwargs):
        indication_form = IndicationForm(request.POST)
        if indication_form.is_valid():
            obj = indication_form.save()
            if request.POST["action"] == "save_and_new":
                indication_form = IndicationForm(
                    initial={
                        "indication_val": obj.indication_val,
                        "service": obj.service,
                    }
                )
                context = {
                    "form": indication_form,
                }
                return render(request, "indication/indication_form.html", context)
            else:
                return redirect("indicators")
        else:
            context = {
                "form": indication_form,
            }
            return render(request, "indication/indication_form.html", context)


class CreateNewIndication(StaffRequiredMixin, CreateView):
    model = Indication
    template_name = "indication/indication_form.html"
    form_class = IndicationForm

    def get_success_url(self):
        category = self.kwargs["category"]
        return "/category/{}".format(category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crate_new_indication"] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        flat = Flat.objects.get(pk=self.kwargs["flat"])
        service = Service.objects.get(pk=self.kwargs["service"])
        initial["house"] = flat.house
        initial["section"] = flat.section
        initial["flat"] = flat
        initial["service"] = service
        return initial

    def post(self, request, *args, **kwargs):
        form = IndicationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.POST["action"] == "save_and_new":
                indication_form = IndicationForm(
                    initial={
                        "indication_val": obj.indication_val,
                        "service": obj.service,
                    }
                )
                context = {
                    "form": indication_form,
                }
                return render(request, "indication/indication_form.html", context)
            else:
                url = reverse("counter_indications", args=[obj.flat.id, obj.service.id])
                return redirect(url)
        else:
            context = {"form": form, "create_new_indication": True}
            return render(request, "indication/indication_form.html", context)


class CreateIndicationForFlat(StaffRequiredMixin, CreateView):
    model = Indication
    template_name = "indication/indication_form.html"
    form_class = IndicationForm

    def get_success_url(self):
        category = self.kwargs["category"]  # Retrieve the category value from the URL
        return "/category/{}/".format(category)  # Build the URL using the retrieved value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_new_indication"] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        flat = Flat.objects.get(pk=self.kwargs["flat"])
        initial["house"] = flat.house
        initial["section"] = flat.section
        initial["flat"] = flat
        return initial

    def post(self, request, *args, **kwargs):
        form = IndicationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.POST["action"] == "save_and_new":
                indication_form = IndicationForm(
                    initial={
                        "indication_val": obj.indication_val,
                        "service": obj.service,
                    }
                )
                data = {"form": indication_form}
                return render(request, "indication/indication_form.html", context=data)
            else:
                url = reverse("flat_indications", args=[obj.flat.id])
                return redirect(url)
        else:
            data = {
                "form": form,
                "create_new_indication": True,
            }
            return render(request, "indication/indication_form.html", context=data)


class UpdateIndication(StaffRequiredMixin, UpdateView):
    model = Indication
    template_name = "indication/indication_form.html"
    form_class = IndicationForm
    success_url = reverse_lazy("indicators")

    def get(self, request, pk, *args, **kwargs):
        obj = Indication.objects.get(pk=pk)
        form = IndicationForm(instance=obj, initial={"house": obj.flat.house, "section": obj.flat.section})
        context = {
            "form": form,
        }
        return render(request, "indication/indication_update.html", context)
