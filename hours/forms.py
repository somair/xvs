from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

from models import TimeRecord, Endorsement

years = xrange(datetime.datetime.now().year - 10, datetime.datetime.now().year + 10)
last_three_years = xrange(datetime.datetime.now().year - 2, datetime.datetime.now().year + 1)

class DateForm(forms.Form):
    date = forms.DateField(widget=SelectDateWidget(years=years), initial=lambda: datetime.datetime.now())

class TimeRecordForm(forms.ModelForm):
    date_worked = forms.DateField(widget=SelectDateWidget(years=last_three_years), initial=lambda: datetime.datetime.now())
    class Meta:
        model = TimeRecord
        exclude = ['confirmed', 'reviewed', 'reviewed_by', 'volunteer']

    def clean(self):
        """Require either an organisation or a manual organisation."""
        cleaned_data = self.cleaned_data
        organisation = cleaned_data.get("organisation")
        manual_organisation = cleaned_data.get("manual_organisation")
        
        if not (organisation or len(manual_organisation)):
            self._errors['organisation'] = self.error_class(["You must either select an organisation from the dropdown, or enter the name of an organisation below."])

        if (organisation and len(manual_organisation)):
            self._errors['organisation'] = self.error_class(["You cannot select an organisation and name an organisation at the same time."])

        return cleaned_data

class EndorsementForm(forms.ModelForm):
    endorsement_text = forms.CharField(widget=forms.Textarea(), label='Endorsement')
    class Meta:
        model = Endorsement
        exclude = ('created, representative', 'position',)
