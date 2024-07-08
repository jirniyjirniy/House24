import django.forms as forms

from src.admin_panel.models import House, Section, FlatOwner, Flat, PersonalAccount


class PersonalAccountsFilterForm(forms.Form):
    STATUS_CHOICE = (
        ('', ''),
        ('active', 'Активен'),
        ('not active', 'Не активен'),
    )
    DEBTS_CHOICE = (
        ('', ''),
        ('yes', 'Есть долг'),
        ('no', 'Нет долга'),

    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0 form-house-select'}))
    section = forms.ModelChoiceField(label="", required=False, queryset=Section.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-section select2-success rounded-0 form-section-select'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    have_debts = forms.ChoiceField(label="", required=False, choices=DEBTS_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class PersonalAccountForm(forms.ModelForm):
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number', 'placeholder': ''}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира', required=False,
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))

    def __init__(self, *args, **kwargs):
        super(PersonalAccountForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."

    class Meta:
        model = PersonalAccount
        fields = '__all__'
        exclude = ('balance',)