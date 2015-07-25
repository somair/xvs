from django import forms
from models import Page

class WebsiteForm(forms.ModelForm):

	status_choices = ((0, 'Draft'),
					(1, 'Published'))

	page_name = forms.CharField(widget=forms.TextInput(attrs={'size': 140}))
	page_content = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 30}))
	status = forms.ChoiceField(choices=status_choices)

	class Meta:
		model = Page
		exclude = ["order",]
