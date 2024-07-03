import datetime

from django.db.models import Sum, Q
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from src.admin_panel.models import Flat, Receipt, ReceiptService


class CabinetStatisticView(TemplateView):
    template_name = 'cabinet/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        previous_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).month
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


class ReceiptList(ListView):
    ...
