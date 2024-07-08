import django.forms as forms
from django.utils import timezone

from src.admin_panel.models import FlatOwner, Receipt, Section, House, Flat, TariffSystem, ReceiptService, Service, \
    Measure, ReceiptExcelDoc


class ReceiptFilterForm(forms.Form):
    COMPLETE = (
        ('', ''),
        ('complete', 'Проведена'),
        ('no complete', 'Не проведена'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('paid', 'Оплачена'),
        ('partially_paid', 'Частично оплачена'),
        ('unpaid', 'Не оплачена'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    month = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'month-picker', 'value': '', 'style': 'background:white'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    complete = forms.ChoiceField(label="", choices=COMPLETE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class ReceiptForm(forms.ModelForm):
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(
                                         attrs={'class': 'publishing-date ignore', 'placeholder': ''}))
    start_date = forms.DateField(label='Период с',
                                 widget=forms.DateInput(attrs={'class': 'start-date ignore', 'placeholder': ''}))
    end_date = forms.DateField(label='Период по',
                               widget=forms.DateInput(attrs={'class': 'end-date ignore', 'placeholder': ''}))
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number ignore', 'placeholder': ''}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира',
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))
    tariff = forms.ModelChoiceField(queryset=TariffSystem.objects.all(), label='Тариф',
                                    widget=forms.Select(attrs={'class': 'form-tariff-select'}))
    personal_account = forms.CharField(label='Лицевой счет', required=False,
                                       widget=forms.TextInput(attrs={'class': 'personal_account', 'placeholder': ''}))
    is_complete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0'}),
                                     required=False,
                                     label='Проведена')
    total_price = forms.DecimalField(
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'total_price'}),
        required=False, label='')

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."
        self.fields['tariff'].empty_label = "Выберите..."
        self.fields['date_published'].initial = timezone.now().date()
        self.fields['start_date'].initial = timezone.now().date()
        self.fields['end_date'].initial = timezone.now().date()
        self.fields['total_price'].initial = 0
        self.fields['is_complete'].initial = True

    class Meta:
        model = Receipt
        fields = '__all__'
        exclude = ('service',)


class ReceiptServiceForm(forms.ModelForm):
    consumption = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'consumption'}),
                                     label='')
    unit_price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'unit_price'}),
                                    label='')
    total_service_price = forms.DecimalField(
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'total_service_price'}),
        required=False, label='')
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='',
                                     widget=forms.Select(attrs={'class': 'form-service-select'}))
    measure = forms.ModelChoiceField(queryset=Measure.objects.all(), label='',
                                     widget=forms.Select(attrs={'class': 'form-measure-select'}))

    def __init__(self, *args, **kwargs):
        super(ReceiptServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].empty_label = "Выберите..."
        self.fields['measure'].empty_label = "Выберите..."

    class Meta:
        model = ReceiptService
        fields = '__all__'
        exclude = ('receipt',)


ReceiptServiceFormset = forms.modelformset_factory(model=ReceiptService, form=ReceiptServiceForm, can_delete=True,
                                                   extra=0)


class ReceiptExcelDocForm(forms.ModelForm):
    class Meta:
        model = ReceiptExcelDoc
        fields = '__all__'
        exclude = ('by_default',)
        widgets = {
            'file': forms.FileInput(attrs={'class': 'excel_file  d-block'}),
            'title': forms.TextInput(attrs={'placeholder': ''})
        }
