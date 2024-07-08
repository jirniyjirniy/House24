from django.db.models import Sum, Q
from django.views.generic import TemplateView

from src.admin_panel.models import House, PersonalAccount, Flat, FlatOwner, Application, Paybox, Receipt


def balances(context):
    total_plus = sum(Paybox.objects.filter(debit_credit='plus', is_complete=True).values_list('total', flat=True))
    total_minus = sum(Paybox.objects.filter(debit_credit='minus', is_complete=True).values_list('total', flat=True))
    context['paybox_balance'] = total_plus - total_minus

    context['personal_accounts_debts'] = sum(
        PersonalAccount.objects.filter(balance__lt=0).values_list('balance', flat=True))

    personal_accounts_plus = sum(
        Paybox.objects.filter(debit_credit='plus', is_complete=True, personal_account__isnull=False).values_list(
            'total', flat=True))
    personal_accounts_minus = sum(
        Receipt.objects.filter(is_complete=True, flat__personal_account__isnull=False).values_list(
            'total_price', flat=True))
    context['personal_accounts_balance'] = personal_accounts_plus - personal_accounts_minus


class StatisticView(TemplateView):
    template_name = 'statistic/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses_count'] = House.objects.all().count()
        context['personal_accounts_count'] = PersonalAccount.objects.all().count()
        context['flats_count'] = Flat.objects.all().count()
        context['flat_owner_count'] = FlatOwner.objects.all().count()
        context['in_work_applications_count'] = Application.objects.filter(status='in work').count()
        context['new_applications_count'] = Application.objects.filter(status='new').count()
        balances(context)

        receipt_minus_by_month = []
        receipt_plus_by_month = []
        for i in range(1, 13):
            receipt_plus = Receipt.objects.aggregate(
                sum=Sum('total_price', filter=Q(date_published__month=i) & Q(is_complete=True) & Q(status="paid")))
            receipt_minus = Receipt.objects.aggregate(
                sum=Sum('total_price', filter=Q(date_published__month=i) & Q(is_complete=True) & Q(status="unpaid")))

            receipt_minus_by_month.append(int(receipt_minus['sum']) if receipt_minus['sum'] else 0)
            receipt_plus_by_month.append(int(receipt_plus['sum']) if receipt_plus['sum'] else 0)

        context['receipt_minus_by_month'] = receipt_minus_by_month
        context['receipt_plus_by_month'] = receipt_plus_by_month

        paybox_minus_by_month = []
        paybox_plus_by_month = []
        for i in range(1, 13):
            paybox_plus = Paybox.objects.aggregate(
                sum=Sum('total', filter=Q(date_published__month=i) & Q(is_complete=True) & Q(debit_credit="plus")))
            paybox_minus = Paybox.objects.aggregate(
                sum=Sum('total', filter=Q(date_published__month=i) & Q(is_complete=True) & Q(debit_credit="minus")))

            paybox_minus_by_month.append(int(paybox_minus['sum']) if paybox_minus['sum'] else 0)
            paybox_plus_by_month.append(int(paybox_plus['sum']) if paybox_plus['sum'] else 0)

        context['paybox_minus_by_month'] = paybox_minus_by_month
        context['paybox_plus_by_month'] = paybox_plus_by_month
        return context
