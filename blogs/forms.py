from django import forms
from models import Entry

#TODO: Rename to BlogForm
class blog_form(forms.ModelForm):

	title = forms.CharField(widget=forms.TextInput(attrs={'size': 126}))
	body = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 20}))

	class Meta:
		model = Entry
		exclude = ('published', 'publisher')
