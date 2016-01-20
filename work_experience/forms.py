import models
from django import forms


class WorkExperienceForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(WorkExperienceForm, self).__init__(*args, **kwargs)
		self.fields['certifications'].help_text = ''
		self.fields['reference_email'].help_text = 'An email will be sent to your referrer in order to confirm your work experience'



	class Meta:
		model = models.WorkExperience
		exclude = ['volunteer', 'skills', 'confirmed']
		widgets = {'certifications': forms.CheckboxSelectMultiple}
