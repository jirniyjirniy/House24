# -*- coding: utf-8 -*-
import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView, View

from src.accounts.forms import RoleFormset

from ..forms.accounts import PersonalFilterForm, PersonalSignUpForm, PersonalUpdateForm
from ..forms.system_settings import (
    MeasureFormset,
    PaymentArticleForm,
    PaymentDetailForm,
    ServicesFormset,
    TariffForm,
    TariffServiceFormset,
)
from ..models.business import *
from .other import StaffRequiredMixin


class ServicesView(StaffRequiredMixin, FormView):
    template_name = "system_settings/services.html"

    def get(self, request, *args, **kw):
        service_formset = ServicesFormset(prefix="service_formset")
        measure_formset = MeasureFormset(prefix="measure_formset")
        context = {
            "service_formset": service_formset,
            "measure_formset": measure_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kw):
        service_formset = ServicesFormset(request.POST, prefix="service_formset")
        measure_formset = MeasureFormset(request.POST, prefix="measure_formset")

        if measure_formset.is_valid():
            instances = measure_formset.save(commit=False)
            # TODO: переделать проверку на удаление через /try except
            for obj in measure_formset.deleted_objects:
                obj.delete()

            for instance in instances:
                if instance.title:
                    instance.save()

        if service_formset.is_valid():
            instances = service_formset.save(commit=False)

            for obj in service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                if instance.title:
                    instance.save()

        else:
            context = {
                "service_formset": service_formset,
                "measure_formset": measure_formset,
            }

            return render(request, self.template_name, context)
        return redirect("services")


def get_measure_options(request):
    measures = Measure.objects.all()  # Получаем все единицы измерения
    data = [{"id": measure.id, "text": measure.title} for measure in measures]
    return JsonResponse(data, safe=False)


class TariffListView(StaffRequiredMixin, ListView):
    template_name = "system_settings/tariffs.html"
    model = TariffSystem

    context_object_name = "tariffs"


class TariffDetail(StaffRequiredMixin, DetailView):
    model = TariffSystem
    template_name = "system_settings/tariff_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tariff = TariffSystem.objects.get(pk=self.kwargs["pk"])

        context["tariff"] = tariff
        context["tariffservices"] = tariff.tariffservice_set.all()
        return context


class DeleteTariffView(StaffRequiredMixin, DeleteView):
    model = TariffSystem
    success_url = reverse_lazy("tariffs")

    def post(self, request, pk, *args, **kwargs):
        TariffService.objects.filter(tariff_id=pk).delete()
        return super().post(request, pk, *args, **kwargs)


class UpdateTariffView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kw):
        tariff = TariffSystem.objects.get(pk=pk)
        tariff_system_form = TariffForm(instance=tariff)
        tariff_service_formset = TariffServiceFormset(
            queryset=TariffService.objects.filter(tariff_id=pk), prefix="tariff_service"
        )

        service_formset = ServicesFormset(prefix="service")

        context = {
            "tariff_form": tariff_system_form,
            "tariff_service_formset": tariff_service_formset,
            "service_formset": service_formset,
        }
        return render(request, "system_settings/tariff_update.html", context)

    def post(self, request, pk, *args, **kw):
        tariff_from = TariffForm(request.POST, instance=TariffSystem.objects.get(pk=pk))
        tariff_service_formset = TariffServiceFormset(request.POST, prefix="tariff_service")
        service_formset = ServicesFormset(prefix="service")
        if tariff_from.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_from.save()
            instances = tariff_service_formset.save(commit=False)
            for obj in tariff_service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.tariff_id = tariff.id
                instance.save()
        else:
            context = {
                "tariff_from": tariff_from,
                "tariff_service_formset": tariff_service_formset,
                "service_formset": service_formset,
            }
            return render(request, "system_settings/tariff_form.html", context)
        return redirect("tariffs")


class CreateTariffView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        tariff_form = TariffForm()
        tariff_service_formset = TariffServiceFormset(queryset=TariffService.objects.none(), prefix="tariff_service")
        service_formset = ServicesFormset(prefix="service")
        data = {
            "tariff_form": tariff_form,
            "tariff_service_formset": tariff_service_formset,
            "service_formset": service_formset,
        }
        return render(request, "system_settings/tariff_form.html", context=data)

    def post(self, request, *args, **kwargs):
        tariff_form = TariffForm(request.POST)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix="tariff_service")
        service_formset = ServicesFormset(prefix="service")
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            obj = tariff_form.save()
            instances = tariff_service_formset.save(commit=False)
            for obj in tariff_service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.tariff_id = obj.id
                instance.save()
        else:
            data = {
                "tariff_form": tariff_form,
                "tariff_service_formset": tariff_service_formset,
                "service_formset": service_formset,
            }
            return render(request, "system_settings/tariff_form.html", context=data)
        return redirect("tariffs")


class GetMeasureView(StaffRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service = Service.objects.get(pk=pk)

        context = {
            "measure": service.measure.title,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


class CopyTariffView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        copy = TariffSystem.objects.get(pk=pk)
        tariff_form = TariffForm(instance=copy)

        tariff_service_formset = TariffServiceFormset(
            queryset=TariffService.objects.filter(tariff_id=pk), prefix="tariff_service"
        )
        service_formset = ServicesFormset(prefix="service")

        context = {
            "tariff_form": tariff_form,
            "tariff_service_formset": tariff_service_formset,
            "service_formset": service_formset,
        }

        return render(request, "system_settings/tariff_copy.html", context)

    def post(self, request, *args, **kwargs):
        tariff_form = TariffForm(request.POST)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix="tariff_service")
        service_formset = ServicesFormset(prefix="service")

        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            obj = tariff_form.save()
            instances = tariff_service_formset.save(commit=False)

            for instance in instances:
                instance.pk = None
                instance.tariff_id = obj.id
                instance.save()
        else:
            context = {
                "tariff_form": tariff_form,
                "tariff_service_formset": tariff_service_formset,
                "service_formset": service_formset,
            }
            return render(request, "system_settings/tariff_copy.html", context)
        return redirect("tariffs")


class PersonalListView(StaffRequiredMixin, ListView):
    template_name = "system_settings/personals.html"
    context_object_name = "personals"
    queryset = Personal.objects.all()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PersonalFilterForm()
        return context


class PersonalSignUpView(StaffRequiredMixin, FormView):
    model = CustomUser
    form_class = PersonalSignUpForm
    template_name = "system_settings/personal_form.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("personals")


# class PersonalUpdateView(UpdateView):
#     model = CustomUser
#     form_class = PersonalUpdateForm
#     template_name = 'system_settings/personal_update.html'
#     success_url = reverse_lazy('personals')
#     queryset = CustomUser.objects.all()
#
#     def get(self, request, pk, *args, **kwargs):
#         user = CustomUser.objects.get(pk=pk)
#         form = PersonalUpdateForm(instance=user, initial={'role': Personal.objects.get(user=user).role})
#         context = {
#             'form': form,
#         }
#         return render(request, self.template_name, context)


class PersonalUpdateView(TemplateView):
    template_name = "system_settings/personal_update.html"

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        form = PersonalUpdateForm(instance=user, initial={"role": Personal.objects.get(user=user).role})
        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        form = PersonalUpdateForm(request.POST, instance=user, request=request)
        if form.is_valid():
            user = form.save()
            return redirect("personals")


class PersonalFilterView(StaffRequiredMixin, ListView):
    template_name = "system_settings/personals.html"
    context_object_name = "personals"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PersonalFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        personals = Personal.objects.all()
        form_filter = PersonalFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["user"]:
                result = form_filter.cleaned_data["user"].split(" ")
                qs.append(Q(Q(user__last_name__in=result) | Q(user__first_name__in=result)))

            if form_filter.cleaned_data["phone"]:
                qs.append(Q(user__phone__icontains=form_filter.cleaned_data["phone"]))
            if form_filter.cleaned_data["email"]:
                qs.append(Q(user__email__icontains=form_filter.cleaned_data["email"]))
            if form_filter.cleaned_data["role"]:
                qs.append(Q(role=form_filter.cleaned_data["role"]))
            if form_filter.cleaned_data["status"]:
                qs.append(Q(user__status=form_filter.cleaned_data["status"]))
            q = Q()
            for item in qs:
                q = q & item
            personals = Personal.objects.filter(q)
        return personals


class PersonalDetailView(StaffRequiredMixin, DetailView):
    model = Personal
    template_name = "system_settings/personal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["personal"] = Personal.objects.get(pk=self.kwargs["pk"])
        return context


class PersonalDeleteView(StaffRequiredMixin, DeleteView):
    success_url = reverse_lazy("personals")
    queryset = Personal.objects.all()


class PaymentDetailView(StaffRequiredMixin, UpdateView):
    template_name = "system_settings/payment_detail.html"
    form_class = PaymentDetailForm
    success_url = reverse_lazy("payment")

    def get_object(self, queryset=None):
        return PaymentDetail.objects.first()


class CreatePaymentArticleView(StaffRequiredMixin, CreateView):
    template_name = "system_settings/article_payment_form.html"
    form_class = PaymentArticleForm
    success_url = reverse_lazy("article_payments")


class ListPaymentArticleView(StaffRequiredMixin, ListView):
    template_name = "system_settings/article_payments.html"
    context_object_name = "payments"
    queryset = Article.objects.all()


class UpdatePaymentArticleView(StaffRequiredMixin, UpdateView):
    template_name = "system_settings/article_payment_update.html"
    form_class = PaymentArticleForm
    success_url = reverse_lazy("article_payments")
    queryset = Article.objects.all()


class DeletePaymentArticleView(StaffRequiredMixin, DeleteView):
    success_url = reverse_lazy("article_payments")
    queryset = Article.objects.all()


class RolesListView(StaffRequiredMixin, FormView):
    template_name = "system_settings/roles.html"

    def get(self, request, *args, **kwargs):
        roles_formset = RoleFormset(prefix="roles")
        context = {
            "roles_formset": roles_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        roles_formset = RoleFormset(request.POST, prefix="roles")
        if roles_formset.is_valid():
            roles_formset.save()
        else:
            context = {
                "roles_formset": roles_formset,
            }
            return render(request, self.template_name, context)
        return redirect("roles")
