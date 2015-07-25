from django import forms

from models import *

class MailoutForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'cols': 74, 'rows': 30}))
	class Meta:
		model = Mailout
        fields = ['subject', 'body']
