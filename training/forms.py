from django import forms
from training import models

class TrainingForm(forms.ModelForm):

	class Meta:
		model = models.Training

class EventForm(forms.ModelForm):

	class Meta:
		model = models.Event