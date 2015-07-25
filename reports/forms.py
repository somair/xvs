from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

years = xrange(datetime.datetime.now().year - 5, datetime.datetime.now().year + 1)

class DateRangeForm(forms.Form):
    date_start = forms.DateField(widget=SelectDateWidget(years=years), initial=lambda: datetime.datetime.now() - datetime.timedelta(days=30))
    date_end   = forms.DateField(widget=SelectDateWidget(years=years), initial=datetime.datetime.now)