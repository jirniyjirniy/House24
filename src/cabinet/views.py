import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Avg
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from weasyprint import HTML, CSS

from src.admin_panel.forms.application import CreateApplicationForm, ApplicationForm
from src.admin_panel.forms.clients import ClientUpdateForm
from src.admin_panel.forms.mail import SearchMessageFilterForm
from src.admin_panel.forms.receipts import ReceiptFilterForm
from src.admin_panel.models import Flat, Receipt, ReceiptService, CustomUser, FlatOwner, Application, MailBox, \
    TariffSystem


class CabinetStatisticView(LoginRequiredMixin, TemplateView):
    template_name = 'cabinet/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        flat = Flat.objects.get(pk=self.kwargs['flat_id'])
        context['flat'] = flat
        if hasattr(flat, 'personal_account'):
            if flat.personal_account is None or flat.personal_account == '':
                context['personal_account'] = 'не указан'
                context['personal_account_balance'] = 'не указан'

            else:
                context['personal_account_balance'] = flat.personal_account.balance
                context['personal_account'] = flat.personal_account.number

        else:
            context['personal_account'] = 'не указан'
            context['personal_account_balance'] = 'не указан'

        receipts_current_year = Receipt.objects.filter(flat=flat, date_published__year=timezone.now().year)
        services = ReceiptService.objects.filter(receipt_id__in=receipts_current_year.values_list('id', flat=True))
        year_consumptions = []
        result = 0
        for service in services.distinct('service_id').values_list('service__title', flat=True):

            for item in services.filter(service__title=service):
                result += int(item.consumption * item.unit_price)
            year_consumptions.append([service, result])
            result = 0
        context['year_consumptions'] = year_consumptions

        previous_month = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).month
        receipts_previous_month = Receipt.objects.filter(flat=flat, date_published__month=previous_month)
        services = ReceiptService.objects.filter(receipt_id__in=receipts_previous_month.values_list('id', flat=True))
        month_consumptions = []
        result = 0
        for service in services.distinct('service_id').values_list('service__title', flat=True):
            for item in services.filter(service__title=service):
                result += int(item.consumption * item.unit_price)
            month_consumptions.append([service, result])
            result = 0
        context['month_consumptions'] = month_consumptions

        year_consumptions_by_month = []
        for i in range(1, 13):
            receipt_by_month = Receipt.objects.filter(flat=flat, date_published__year=timezone.now().year).aggregate(
                sum=Sum('total_price', filter=Q(date_published__month=i) & Q(is_complete=True)))

            year_consumptions_by_month.append(int(receipt_by_month['sum']) if receipt_by_month['sum'] else 0)

        context['year_consumptions_by_month'] = year_consumptions_by_month
        avg_consumption_for_month = Receipt.objects.filter(flat=flat,
                                                           date_published__year=timezone.now().year).aggregate(
            sum=Sum('total_price', filter=Q(is_complete=True)))
        context['avg_consumption_for_month'] = 0 if avg_consumption_for_month['sum'] is None else round(
            avg_consumption_for_month['sum'] / 12, 2)
        return context


class ReceiptListCabinet(LoginRequiredMixin, ListView):
    template_name = 'cabinet/receipts.html'
    context_object_name = 'receipts'
    paginate_by = 20

    def get_queryset(self):
        client = self.request.user.client
        result = Receipt.objects.filter(flat__flat_owner_id=client.id)
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        context['filter_form'] = ReceiptFilterForm()
        return context


class FlatReceiptList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/flat_receipts.html'
    context_object_name = 'receipts'
    paginate_by = 20

    def get_queryset(self):
        client = self.request.user.client
        result = Receipt.objects.filter(flat__flat_owner_id=client.id, flat_id=self.kwargs['flat_id'])
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ReceiptFilterForm()
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        context['flat_id'] = self.kwargs['flat_id']
        return context


class FlatReceiptFilteredList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/flat_receipts.html'
    context_object_name = 'receipts'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ReceiptFilterForm(initial=self.request.GET)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        context['flat_id'] = self.kwargs['flat_id']
        return context

    def get_queryset(self):
        client = self.request.user.client
        receipts = Receipt.objects.filter(flat__flat_owner_id=client.id, flat_id=self.kwargs['flat_id'])
        form_filter = ReceiptFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data['status']:
                qs.append(Q(status=form_filter.cleaned_data['status']))
            if form_filter.cleaned_data['daterange']:
                date_start, date_end = str(form_filter.cleaned_data['daterange']).split(' - ')
                date_start = date_start.split('/')
                date_end = date_end.split('/')
                date_start.reverse()
                date_end.reverse()
                date_start = "-".join(date_start)
                date_end = "-".join(date_end)
                qs.append(Q(
                    Q(date_published__gte=date_start) &
                    Q(date_published__lte=date_end)
                ))
            q = Q()
            for item in qs:
                q = q & item
            receipts = receipts.filter(q)
        return receipts


class CabinetReceiptsFilteredList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/receipts.html'
    context_object_name = 'receipts'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        context['filter_form'] = ReceiptFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        client = self.request.user.client
        receipts = Receipt.objects.filter(flat__flat_owner_id=client.id)
        form_filter = ReceiptFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data['status']:
                qs.append(Q(status=form_filter.cleaned_data['status']))
            if form_filter.cleaned_data['daterange']:
                date_start, date_end = str(form_filter.cleaned_data['daterange']).split(' - ')
                date_start = date_start.split('/')
                date_end = date_end.split('/')
                date_start.reverse()
                date_end.reverse()
                date_start = "-".join(date_start)
                date_end = "-".join(date_end)
                qs.append(Q(
                    Q(date_published__gte=date_start) &
                    Q(date_published__lte=date_end)
                ))
            q = Q()
            for item in qs:
                q = q & item
            receipts = receipts.filter(q)
        return receipts


class CabinetReceiptDetail(LoginRequiredMixin, DetailView):
    model = Receipt
    template_name = 'cabinet/receipts_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipt = Receipt.objects.get(pk=self.kwargs['pk'])
        receipt_services = ReceiptService.objects.filter(receipt_id=self.kwargs['pk'])
        context['receipt'] = receipt
        context['receipt_services'] = receipt_services
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return context


class ReceiptPDF(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        receipt = Receipt.objects.get(pk=self.kwargs['receipt_id'])
        services = ReceiptService.objects.filter(receipt_id=self.kwargs['receipt_id'])
        html_template = get_template('cabinet/invoice.html')
        context = {
            'services': services,
            'receipt': receipt,
        }
        html = html_template.render(context).encode(encoding="UTF-8")
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf('media/invoice/invoice.pdf')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="invoice.pdf"'
        return response


class ReceiptPDF2(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        receipt = Receipt.objects.get(pk=self.kwargs['receipt_id'])
        services = ReceiptService.objects.filter(receipt_id=self.kwargs['receipt_id'])
        html_template = get_template('cabinet/invoice.html')
        context = {
            'services': services,
            'receipt': receipt,
        }
        html = html_template.render(context).encode(encoding="UTF-8")
        pdf_file = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="invoice.pdf"'
        return response


class Invoice(LoginRequiredMixin, TemplateView):
    template_name = 'cabinet/invoice.html'


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'cabinet/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ClientUpdateForm
    template_name = 'cabinet/update_profile.html'
    success_url = reverse_lazy('profile')
    queryset = CustomUser.objects.all()

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        owner = FlatOwner.objects.get(user=user)
        form = ClientUpdateForm(instance=user,
                                initial={'birthday': owner.birthday, 'viber': owner.viber, 'telegram': owner.telegram,
                                         'patronymic': owner.patronymic, 'ID': owner.ID,
                                         'bio': owner.bio, })
        data = {
            'form': form,
        }
        return render(request, 'cabinet/update_profile.html', context=data)


class CabinetApplicationList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/applications.html'
    context_object_name = 'applications'
    paginate_by = 20

    def get_queryset(self):
        client = self.request.user.client.id
        return Application.objects.filter(flat__flat_owner_id=client)


class CabinetCreateApplication(LoginRequiredMixin, CreateView):
    model = Application
    template_name = 'cabinet/application_form.html'
    form_class = CreateApplicationForm

    def get(self, request, *args, **kwargs):
        form = CreateApplicationForm()
        client = request.user.client
        form.fields['flat'].queryset = Flat.objects.filter(flat_owner_id=client.id)

        context = {
            'form': form,
        }

        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return render(request, 'cabinet/application_form.html', context)

    success_url = reverse_lazy('applications_cabinet')


class CabinetMailboxList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/mailbox.html'
    context_object_name = 'mailboxes'

    def get_queryset(self):
        result = MailBox.objects.filter(flat_owners__user_id=self.request.user.id)
        return result

    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = SearchMessageFilterForm()
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return context


class CabinetMailboxFilteredList(LoginRequiredMixin, ListView):
    template_name = 'cabinet/mailbox.html'
    context_object_name = 'mailboxes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = SearchMessageFilterForm(initial=self.request.GET)
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return context

    def get_queryset(self):
        search_filter = SearchMessageFilterForm(self.request.GET)
        mailboxes = MailBox.objects.filter(flat_owners__user_id=self.request.user.id)
        qs = []
        if search_filter.is_valid():
            if search_filter.cleaned_data['search_row']:
                qs.append(Q(description__icontains=search_filter.cleaned_data['search_row']))
                qs.append(Q(title__icontains=search_filter.cleaned_data['search_row']))
            q = Q()
            for item in qs:
                q = q | item
            mailboxes = mailboxes.filter(q)
        return mailboxes


class CabinetMailboxDetail(LoginRequiredMixin, DetailView):
    model = MailBox
    template_name = 'cabinet/mailbox_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = MailBox.objects.get(pk=self.kwargs['pk'])
        obj.unread = False
        obj.save()
        context['mailbox'] = obj
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)
        return context


class CabinetDeleteMailbox(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('mailboxes_cabinet')
    def post(self, request, pk, *args, **kwargs):
        obj = MailBox.objects.get(pk=pk)
        obj.flat_owners.remove(self.request.user.client)
        obj.save()
        context = {
            'mailboxes': MailBox.objects.filter(flat_owners__users_id=self.request.user.id)
        }
        return render(request, 'cabinet/mailbox.html', context)


class CabinetTariffDetail(LoginRequiredMixin, TemplateView):
    model = TariffSystem
    template_name = 'cabinet/tariff_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flat = Flat.objects.get(pk=self.kwargs['flat_id'])
        context['flat'] = flat
        context['flats'] = Flat.objects.filter(flat_owner__user=self.request.user)

        if flat.tariff:
            context['tariff'] = flat.tariff
            context['tariffservices'] = flat.tariff.tariffservice_set.all()
        else:
            context['tariff'] = None
            context['tariffservices'] = None
        return context
