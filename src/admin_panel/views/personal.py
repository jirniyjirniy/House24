# -*- coding: utf-8 -*-
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from src.admin_panel.models import PersonalAccount

from ..forms.personal import PersonalAccountFilterForm, PersonalAccountForm


class PersonalAccountListView(ListView):
    template_name = "personal/personals_list.html"
    context_object_name = "personal_accounts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PersonalAccountFilterForm()
        context["personal_accounts_count"] = PersonalAccount.objects.all().count()
        return context

    def get_queryset(self):
        personal_accounts = PersonalAccount.objects.all()

        for obj in personal_accounts:
            if obj.house is None:
                house = ""
            else:
                house = obj.house
            if obj.section is None:
                section = ""
            else:
                section = obj.section
            if obj.flat is None:
                flat = ""
            else:
                flat = obj.flat
                if obj.flat.flat_owner is not None:
                    flat_owner = obj.flat.flat_owner
                else:
                    flat_owner = ""

        return personal_accounts


class PersonalAccountFilteredList(ListView):
    template_name = "personal/personals_list.html"
    context_object_name = "personal_accounts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PersonalAccountFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        personal_accounts = PersonalAccount.objects.all()
        form_filter = PersonalAccountFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["number"]:
                qs.append(Q(number__icontains=form_filter.cleaned_data["number"]))
            if form_filter.cleaned_data["status"]:
                qs.append(Q(status=form_filter.cleaned_data["status"]))
            if form_filter.cleaned_data["flat"]:
                qs.append(Q(flat__number=form_filter.cleaned_data["flat"]))
            if form_filter.cleaned_data["house"]:
                qs.append(Q(house_id=form_filter.cleaned_data["house"].id))
            if form_filter.cleaned_data["section"]:
                qs.append(Q(section_id=form_filter.cleaned_data["section"].id))
            if form_filter.cleaned_data["flat_owner"]:
                full_name = str(form_filter.cleaned_data["flat_owner"]).split()
                qs.append(
                    Q(
                        Q(flat__flat_onwer__patronymic=full_name[2])
                        & Q(flat__flat_owner_user__first_name=full_name[1])
                        & Q(flat__flat_owner_user__last_name=full_name[0])
                    )
                )
            if form_filter.cleaned_data["have_debts"]:
                if form_filter.cleaned_data["have_debts"] == "no":
                    qs.append(Q(debts__gte=0))
                elif form_filter.cleaned_data["have_debts"] == "yes":
                    qs.append(Q(debts__lt=0))
            q = Q()
            for obj in qs:
                q = q & obj
            personal_accounts = PersonalAccount.objects.filter(q)
        return personal_accounts


class PersonalCreateView(FormView):
    model = PersonalAccount
    template_name = "personal/personal_form.html"
    form_class = PersonalAccountForm
    success_url = reverse_lazy("personal_accounts")
