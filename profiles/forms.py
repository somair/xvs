from django import forms
from models import Faculty, VolunteerProfile, RepresentativeProfile, GRAD_CHOICES, INTERNATIONAL_CHOICES, VOLUNTEER_COLUMN_CHOICES, VOLUNTEER_COLUMN_CHOICES_DEFAULT, YEAR_CHOICES
from positions.models import Organisation, PositionCategory

class VolunteerProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=PositionCategory.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = VolunteerProfile
        exclude = ['profile']

    def clean(self):
        # Extra clean code for universities that enable 
        # the staff and/or recent graduate options.
        cleaned_data = super(VolunteerProfileForm, self).clean()
        postgrad = cleaned_data.get("postgrad")
        international = cleaned_data.get("international")
        year = cleaned_data.get("year")

        if international == "S" or international == "R":
            # Staff members should be neither PG nor UG
            if postgrad != None:
                self._errors["postgrad"] = self.error_class(["You cannot be a postgraduate or undergraduate if you are a staff member! Choose 'non-student' instead."])
            # Staff members should not specify a graduation year
            if year:
                self._errors["year"] = self.error_class(["You should not choose a graduation year if you are not a current student!"])
        else:
            # Non-staff members must choose a grad status.
            if postgrad == None:
                self._errors["postgrad"] = self.error_class(["You must choose either postgraduate or undergraduate."])

        return cleaned_data

class VolunteerProfileUpdateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=PositionCategory.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = VolunteerProfile
        exclude = ['profile', 'referrer']

class RepresentativeProfileForm(forms.ModelForm):
    class Meta:
        model = RepresentativeProfile
        exclude = ['profile', 'organisation']

class OrganisationProfileForm(forms.ModelForm):
    class Meta:
        model = Organisation
        exclude = ['name']

class VolunteerTypeFilterForm(forms.Form):
    postgrad = forms.MultipleChoiceField(required=False, choices=GRAD_CHOICES, widget=forms.CheckboxSelectMultiple)
    international = forms.MultipleChoiceField(required=False, choices=INTERNATIONAL_CHOICES, widget=forms.CheckboxSelectMultiple)
    course = forms.CharField(max_length=63, required=False)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=PositionCategory.objects.all(), required=False)
    hours = forms.ChoiceField(initial="BOTH", choices=(("BOTH", "have and have not logged hours"), ("HAS_HOURS", "have logged hours"), ("NO_HOURS", "have not logged hours")), required=False)
    year = forms.ChoiceField(initial=None, choices=[("ALL", "any year")] + list(YEAR_CHOICES), required=False)

class ColumnFilterForm(forms.Form):
    columns = forms.MultipleChoiceField(required=False, choices=VOLUNTEER_COLUMN_CHOICES, widget=forms.CheckboxSelectMultiple)
