import django.forms as forms
from django.utils import timezone

from datetime import datetime

from src.admin_panel.models import FlatOwner, Flat, Personal, Application


class FlatChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.application_label()


class PersonalChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.application_label()


class ApplicationForm(forms.ModelForm):
    ROLE_CHOICE = (
        ('', 'Любой специалист'),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
        ('locksmith', 'Слесарь'),
    )
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(attrs={'class': 'publishing-date', 'placeholder': ''}))
    time_published = forms.TimeField(label='',
                                     widget=forms.TimeInput(attrs={'class': 'publishing-time', 'placeholder': ''}))
    flat_owner = forms.ModelChoiceField(queryset=FlatOwner.objects.all(), label='Владелец квартиры ', required=False,
                                        widget=forms.Select(attrs={'class': 'form-flat_owner-select select2'}))

    flat = FlatChoiceField(queryset=Flat.objects.filter(house__isnull=False), label='Квартира',
                           widget=forms.Select(attrs={'class': 'form-flat-select select2'}))

    user = PersonalChoiceField(queryset=Personal.objects.all(), label='Мастер', required=False,
                               widget=forms.Select(attrs={'class': 'form-master-select'}))

    user_type = forms.ChoiceField(choices=ROLE_CHOICE, label='Тип мастера', required=False, )
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '', 'rows': 8}), label='Описание')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."
        self.fields['flat_owner'].empty_label = "Выберите..."
        self.fields['user'].empty_label = "Выберите..."

    class Meta:
        model = Application
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '', 'rows': 8, 'class': 'summernote'})
        }


class CreateApplicationForm(ApplicationForm):
    def __init__(self, *args, **kwargs):
        ApplicationForm.__init__(self, *args, **kwargs)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Выберите...'
        self.fields['date_published'].initial = timezone.now().date()
        self.fields['time_published'].initial = timezone.now().time()


class ApplicationsFilterForm(forms.Form):
    ROLE_CHOICE = (
        ('', ''),
        ('any_master', 'Любой специалист'),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
        ('locksmith', 'Слесарь'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('new', 'Новое'),
        ('in work', 'В работе'),
        ('complete', 'Выполнено'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    master_type = forms.ChoiceField(label="", required=False, choices=ROLE_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    description = forms.CharField(label="", max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control  rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    phone = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    master = PersonalChoiceField(label="", required=False, queryset=Personal.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
