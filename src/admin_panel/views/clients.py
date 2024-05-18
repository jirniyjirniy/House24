# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..forms.clients import ClientsFilterForm, ClientSignUpForm, ClientUpdateForm
from ..models.accounts import CustomUser, FlatOwner


class ClientsListView(ListView):
    template_name = "clients/clients_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["filter_form"] = ClientsFilterForm()
        return context

    def get_queryset(self):
        clients = FlatOwner.objects.all()
        return clients


class ClientsFilteredListView(ListView):
    template_name = "clients/clients_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ClientsFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        clients = FlatOwner.objects.all()
        form_filter = ClientsFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data["ID"]:
                qs.append(Q(ID__icontains=form_filter.cleaned_data["ID"]))
            if form_filter.cleaned_data["full_name"]:
                full_name = form_filter.cleaned_data["full_name"].split(" ")
                qs.append(
                    Q(
                        Q(patronymic__icontains=form_filter.cleaned_data["full_name"])
                        | Q(patronymic__in=full_name)
                        | Q(user__first_name__in=full_name)
                        | Q(user__last_name__in=full_name)
                        | Q(user__first_name__icontains=form_filter.cleaned_data["full_name"])
                        | Q(user__last_name__icontains=form_filter.cleaned_data["full_name"])
                    )
                )

            if form_filter.cleaned_data["phone"]:
                qs.append(Q(user__phone__icontains=form_filter.cleaned_data["phone"]))
            if form_filter.cleaned_data["email"]:
                qs.append(Q(user__email=form_filter.cleaned_data["email"]))
            if form_filter.cleaned_data["house"]:
                qs.append(Q(flat__house_id=form_filter.cleaned_data["house"].id))
            if form_filter.cleaned_data["flat"]:
                qs.append(Q(flat__number=form_filter.cleaned_data["flat"]))
            if form_filter.cleaned_data["status"]:
                qs.append(Q(user__status=form_filter.cleaned_data["status"]))
            if form_filter.cleaned_data["date_added"]:
                date_str = form_filter.cleaned_data["date_added"].split("/")
                date_str.reverse()
                result = "-".join(date_str)
                qs.append(Q(user__date_joined=result))

            q = Q()
            for item in qs:
                q = q & item
            clients = FlatOwner.objects.filter(q)
        return clients


class ClientDetailView(DetailView):
    model = FlatOwner
    template_name = "clients/clients_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = FlatOwner.objects.prefetch_related("flat_set").get(pk=self.kwargs["pk"])

        context["client"] = client
        context["flats"] = client.flat_set.all()
        return context


class ClientSignUpView(CreateView):
    model = CustomUser
    form_class = ClientSignUpForm
    template_name = "clients/clients_form.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("clients")


class ClientUpdateView(UpdateView):
    model = CustomUser
    form_class = ClientUpdateForm
    template_name = "clients/client_update.html"
    success_url = reverse_lazy("clients")
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.kwargs["pk"])
        owner = FlatOwner.objects.get(user=user)

        form = ClientUpdateForm(
            instance=user,
            initial={
                "birthday": owner.birthday,
                "viber": owner.viber,
                "telegram": owner.telegram,
                "patronymic": owner.patronymic,
                "ID": owner.ID,
                "bio": owner.bio,
            },
        )
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class DeleteClientView(DeleteView):
    success_url = reverse_lazy("clients")
    queryset = CustomUser.objects.all()
