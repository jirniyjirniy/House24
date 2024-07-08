from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView

from src.admin_panel.forms.mail import MailSearchForm, MailBoxForm
from src.admin_panel.models import MailBox, Personal


class MailListView(ListView):
    template_name = 'mailing/mails.html'
    context_object_name = 'mails'
    queryset = MailBox.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MailSearchForm()
        return context


class MailFilteredListView(ListView):
    template_name = 'mailing/mails.html'
    context_object_name = 'mails'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MailSearchForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        search_form = MailSearchForm(self.request.GET)
        mailboxes = MailBox.objects.all()
        qs = []
        if search_form.is_valid():
            if search_form.cleaned_data['search_row']:
                qs.append(Q(description__icontains=search_form.cleaned_data['search_row']))
                qs.append(Q(title__icontains=search_form.cleaned_data['search_row']))
            q = Q()

            for item in qs:
                q = q | item
            mailboxes = MailBox.objects.filter(q)
        return mailboxes


class MailCreateView(CreateView):
    model = MailBox
    template_name = 'mailing/mail_create.html'
    form_class = MailBoxForm
    success_url = reverse_lazy('mailbox')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender_id = Personal.objects.get(user_id=self.request.user.id).id
        obj.save()
        return super().form_valid(form)


class MailDebtorsCreateView(CreateView):
    model = MailBox
    template_name = 'mailing/mail_create.html'
    success_url = reverse_lazy('mailbox')

    def get(self, request, *args, **kwargs):
        form = MailBoxForm()
        form.fields['to_debtors'].initial = True
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender_id = Personal.objects.get(user_id=self.request.user.id).id
        obj.save()
        return super().form_valid(form)


class MailDetailView(DetailView):
    model = MailBox
    template_name = 'mailing/mail_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailbox'] = MailBox.objects.get(pk=self.kwargs['pk'])
        return context


class MailDeleteView(DeleteView):
    success_url = reverse_lazy('mailbox')
    queryset = MailBox.objects.all()
