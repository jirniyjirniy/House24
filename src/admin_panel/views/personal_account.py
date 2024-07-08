from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from openpyxl.styles import Font

from src.admin_panel.forms.personal_account import PersonalAccountsFilterForm, PersonalAccountForm
from src.admin_panel.models import PersonalAccount, Paybox, Receipt
from openpyxl import Workbook


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


class PersonalAccountListView(ListView):
    template_name = 'personal_account/personal_accounts.html'
    context_object_name = 'personal_accounts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PersonalAccountsFilterForm()
        context['personal_accounts_count'] = PersonalAccount.objects.all().count()
        balances(context)
        return context

    def get_queryset(self):
        personal_accounts = PersonalAccount.objects.all()

        wb = Workbook()
        ws = wb.active
        ws.append([
            'Лицевой счет',
            'Статус',
            'Дом',
            'Секция',
            'Квартира',
            'Владелец',
            'Остаток',
        ])
        bold_font = Font(bold=True)
        for cell in ws[1]:
            cell.font = bold_font

        for obj in personal_accounts:
            if obj.house is None:
                house = f''
            else:
                house = f'{obj.house}'

            if obj.section is None:
                section = f''
            else:
                section = f'{obj.section}'

            if obj.flat is None:
                flat = f''
            else:
                flat = f'{obj.flat}'

            if obj.flat is not None:
                if obj.flat.flat_owner is not None:
                    flat_owner = f'{obj.flat.flat_owner}'
                else:
                    flat_owner = ''
            else:
                flat_owner = ''

            ws.append([
                f'{obj.number}',
                f'{obj.get_status_display()}',
                f'{house}',
                f'{section}',
                f'{flat}',
                f'{flat_owner}',
                f'{obj.balance}',
            ])

        ws.title = 'Выписка'
        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 30
        ws.column_dimensions['G'].width = 20

        wb.save('media/personal_account/info.xlsx')
        wb.close()

        return personal_accounts


class PersonalAccountFilteredListView(ListView):
    template_name = 'personal_account/personal_accounts.html'
    context_object_name = 'personal_accounts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PersonalAccountsFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        personal_accounts = PersonalAccount.objects.all()
        form_filter = PersonalAccountsFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data['number']:
                qs.append(Q(number__icontains=form_filter.cleaned_data['number']))
            if form_filter.cleaned_data['status']:
                qs.append(Q(status=form_filter.cleaned_data['status']))
            if form_filter.cleaned_data['flat']:
                qs.append(Q(flat__number=form_filter.cleaned_data['flat']))
            if form_filter.cleaned_data['house']:
                qs.append(Q(house_id=form_filter.cleaned_data['house'].id))
            if form_filter.cleaned_data['section']:
                qs.append(Q(section_id=form_filter.cleaned_data['section'].id))
            if form_filter.cleaned_data['flat_owner']:
                full_name = str(form_filter.cleaned_data['flat_owner']).split()
                qs.append(Q(
                    Q(flat__flat_owner__patronymic=full_name[2]) &
                    Q(flat__flat_owner__user__first_name=full_name[1]) &
                    Q(flat__flat_owner__user__last_name=full_name[0])
                ))
            if form_filter.cleaned_data['have_debts']:
                if form_filter.cleaned_data['have_debts'] == 'no':
                    qs.append(Q(balance__gte=0))
                elif form_filter.cleaned_data['have_debts'] == 'yes':
                    qs.append(Q(balance__lt=0))
            q = Q()
            for item in qs:
                q = q & item
            personal_accounts = PersonalAccount.objects.filter(q)
        return personal_accounts


class PersonalAccountDetailView(DetailView):
    model = PersonalAccount
    template_name = 'personal_account/personal_accounts_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal_account = PersonalAccount.objects.get(pk=self.kwargs['pk'])
        context['personal_account'] = personal_account
        return context


class CreatePersonalAccountView(CreateView):
    model = PersonalAccount
    template_name = 'personal_account/personal_account_form.html'
    form_class = PersonalAccountForm
    success_url = reverse_lazy('personal_accounts')


class UpdatePersonalAccountView(UpdateView):
    model = PersonalAccount
    template_name = 'personal_account/personal_account_form.html'
    form_class = PersonalAccountForm
    success_url = reverse_lazy('personal_accounts')


class DeletePersonalAccount(DeleteView):
    success_url = reverse_lazy('personal_accounts')
    queryset = PersonalAccount.objects.all()
