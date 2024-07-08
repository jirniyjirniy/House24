import django.forms as forms

from src.admin_panel.forms.application import PersonalChoiceField
from src.admin_panel.models import Paybox, Article, Personal, FlatOwner, PersonalAccount


class PayboxFilterForm(forms.Form):
    PLUS_MINUS = (
        ('', ''),
        ('plus', 'Приход'),
        ('minus', 'Расход'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('complete', 'Проведен'),
        ('no complete', 'Не проведен'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    article = forms.ModelChoiceField(label='', queryset=Article.objects.all(), required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    personal_account = forms.CharField(label="", max_length=100, required=False,
                                       widget=forms.TextInput(
                                           attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    debit_credit = forms.ChoiceField(label="", choices=PLUS_MINUS, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class PayboxForm(forms.ModelForm):
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(
                                         attrs={'class': 'publishing-date ignore', 'placeholder': ''}))
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number ignore', 'placeholder': ''}))
    personal_account = forms.ModelChoiceField(label='Лицевой счет', queryset=PersonalAccount.objects.all(),
                                              required=False,
                                              widget=forms.Select(
                                                  attrs={'class': 'personal_account-select select2',
                                                         'placeholder': ''}))
    flat_owner = forms.ModelChoiceField(label='Владелец квартиры', queryset=FlatOwner.objects.all(), required=False,
                                        widget=forms.Select(attrs={'class': 'form-flat_owner-select select2',
                                                                   'placeholder': ''}))
    user = PersonalChoiceField(label='Менеджер', required=False,
                               queryset=Personal.objects.filter(role__in=['director', 'accountant', 'manager']),
                               widget=forms.Select(attrs={'class': 'personal_account', 'placeholder': ''}))
    article = forms.ModelChoiceField(label='Статья', queryset=Article.objects.all(),
                                     widget=forms.Select(attrs={'class': 'personal_account', 'placeholder': ''}))
    is_complete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0'}),
                                     required=False,
                                     label='Проведен')

    total = forms.DecimalField(label='Сумма', widget=forms.NumberInput(attrs={'placeholder': ''}))

    def __init__(self, *args, **kwargs):
        super(PayboxForm, self).__init__(*args, **kwargs)
        self.fields['article'].empty_label = 'Выберите...'
        self.fields['personal_account'].empty_label = 'Выберите...'
        self.fields['flat_owner'].empty_label = 'Выберите...'
        self.fields['user'].empty_label = 'Выберите...'

    class Meta:
        model = Paybox
        fields = '__all__'
        exclude = ('debit_credit',)
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '', 'rows': 5, })
        }
