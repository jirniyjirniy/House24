import django.forms as forms
from django.db.models import Q

from src.admin_panel.models import House, Section, Floor, Flat, MailBox


class MailSearchForm(forms.Form):
    search_row = forms.CharField(label='', max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))


class MailBoxForm(forms.ModelForm):
    to_debtors = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'to_debtors rounded-0 shadow-none'}),
                                    required=False,
                                    label='Владельцам с задолженностями')
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='ЖК', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), label='Этаж', required=False,
                                   widget=forms.Select(attrs={'class': 'form-floor-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира', required=False,
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))

    def __init__(self, *args, **kwargs):
        super(MailBoxForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Всем..."
        self.fields['section'].empty_label = "Всем..."
        self.fields['floor'].empty_label = "Всем..."
        self.fields['flat'].empty_label = "Всем..."

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            flats = Flat.objects.filter(flat_owner__isnull=False)
            if self.cleaned_data['to_debtors']:
                flats = flats.filter(personal_account__balance__lt=0)
            q = []
            if self.cleaned_data['house']:
                q.append(Q(house=self.cleaned_data['house']))
                if self.cleaned_data['section']:
                    q.append(Q(section=self.cleaned_data['section']))
                if self.cleaned_data['floor']:
                    q.append(Q(floor=self.cleaned_data['floor']))
                if self.cleaned_data['flat']:
                    q.append(Q(id=self.cleaned_data['flat'].id))
                result = Q()
                for item in q:
                    result = result & item
                flats = flats.filter(result)
            for flat in flats:
                instance.flat_owners.add(flat.flat_owner)
        return instance

    class Meta:
        model = MailBox
        fields = ('title', 'description', 'house', 'section', 'floor', 'flat')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Тема сообщения'}),
            'description': forms.Textarea(attrs={'placeholder': 'Текст сообщения:', 'class': 'summernote'})
        }


class SearchMessageFilterForm(forms.Form):
    search_row = forms.CharField(label='', max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
