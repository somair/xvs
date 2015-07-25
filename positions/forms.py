from django import forms

from models import *

import settings

class PositionForm(forms.ModelForm):
    oneoff = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                       choices=((0, 'Opportunity is a regular weekly position'), (1, 'This is a one-off opportunity')),
                       widget=forms.RadioSelect
                    )

    def clean(self):
        category = self.cleaned_data.get('category')
        if category and category.count() > 3:
            self._errors['category'] = self.error_class(["""Please choose no more than three categories."""])
            del self.cleaned_data['category']

        return self.cleaned_data

    class Meta:
        model = Position
        exclude = ['organisation', 'representative', 'approved', 'active', 'plus_eligible']
        widgets = {
            "skills_gained": forms.CheckboxSelectMultiple,
            "latlong": forms.HiddenInput,
            "category": forms.CheckboxSelectMultiple,
        }

class PositionFilterForm(forms.Form):
    approved = forms.MultipleChoiceField(choices=(('a', "Approved"), ('u', "Unapproved")), initial=['a', 'u'], widget=forms.CheckboxSelectMultiple)
    listed = forms.MultipleChoiceField(choices=(('l', "Active"), ('d', "De-listed")), initial=['l'], widget=forms.CheckboxSelectMultiple)

    if settings.FEATURE_ORGANISATION_CATEGORIES:
        categories = forms.ModelMultipleChoiceField(queryset=OrganisationCategory.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

class PositionCategoryForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=PositionCategory.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class ColumnFilterForm(forms.Form):
    columns = forms.MultipleChoiceField(required=False, choices=POSITION_COLUMN_CHOICES, widget=forms.CheckboxSelectMultiple)
