from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from src.admin_panel.forms.application import ApplicationsFilterForm, CreateApplicationForm, ApplicationForm
from src.admin_panel.models import Application


class ApplicationListView(ListView):
    template_name = 'application/applications.html'
    context_object_name = 'applications'
    queryset = Application.objects.all()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ApplicationsFilterForm()
        return context


class ApplicationFilteredListView(ListView):
    template_name = 'application/applications.html'
    context_object_name = 'applications'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ApplicationsFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        applications = Application.objects.all()
        form_filter = ApplicationsFilterForm(self.request.GET)
        qs = []

        if form_filter.is_valid():
            if form_filter.cleaned_data['number']:
                qs.append(Q(pk__icontains=form_filter.cleaned_data['number']))
            if form_filter.cleaned_data['daterange']:
                date_start, date_end = str(form_filter.cleaned_data['daterange']).split(' - ')
                date_start = date_start.split('/')
                date_end = date_end.split('/')
                date_start.reverse()
                date_end.reverse()
                date_start = '-'.join(date_start)
                date_end = '-'.join(date_end)
                qs.append(Q(
                    Q(date_published__gte=date_start) &
                    Q(date_published__lte=date_end)
                ))

            if form_filter.cleaned_data['master_type']:
                if form_filter.cleaned_data['master_type'] == 'any_master':
                    qs.append(Q(user_type=''))
                else:
                    qs.append(Q(user_type=form_filter.cleaned_data['master_type']))
            if form_filter.cleaned_data['description']:
                qs.append(Q(description__icontains=form_filter.cleaned_data['description']))
            if form_filter.cleaned_data['flat']:
                qs.append(Q(flat__number__icontains=form_filter.cleaned_data['flat']))
            if form_filter.cleaned_data['flat_owner']:
                full_name = str(form_filter.cleaned_data['flat_owner']).split(' ')
                qs.append(Q(
                    Q(flat__flat_owner__user__last_name__icontains=full_name[0]) &
                    Q(flat__flat_owner__user__first_name__icontains=full_name[1]) &
                    Q(flat__flat_owner__user__patronymic__icontains=full_name[2])
                ))
            if form_filter.cleaned_data['phone']:
                qs.append(Q(flat__flat_owner__user__phone__icontains=form_filter.cleaned_data['phone']))
            if form_filter.cleaned_data['master']:
                full_name = str(form_filter.cleaned_data['master']).split(' ')
                qs.append(Q(
                    Q(user__user__first_name__icontains=full_name[1]) &
                    Q(user__user__last_name__icontains=full_name[0])
                ))
            if form_filter.cleaned_data['status']:
                qs.append(Q(status=form_filter.cleaned_data['status']))

            q = Q()
            for obj in qs:
                q = q & obj
            applications = Application.objects.filter(q)
        return applications


class ApplicationDetailView(DetailView):
    model = Application
    template_name = 'application/application_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = Application.objects.get(pk=self.kwargs['pk'])
        context['application'] = application
        return context


class ApplicationCreateView(CreateView):
    model = Application
    template_name = 'application/application_create.html'
    form_class = CreateApplicationForm
    success_url = reverse_lazy('applications')


class ApplicationUpdateView(UpdateView):
    model = Application
    template_name = 'application/application_update.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('applications')


class ApplicationDeleteView(DeleteView):
    success_url = reverse_lazy('applications')
    queryset = Application.objects.all()

