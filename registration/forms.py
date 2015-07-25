"""
Forms and validation code for user registration.

"""


from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from settings import ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH, SERVER_EMAIL


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']

# Form for Volunteering website registrations.
class RegistrationFormVolunteering(RegistrationFormUniqueEmail):
    def clean(self):
        cleaned_data = self.cleaned_data
        reg_type = cleaned_data.get("reg_type")
        email = cleaned_data.get("email")
        organisation = cleaned_data.get("organisation")

        # If registering as a volunteer, the email address must be at sms.ed.ac.uk.
        if email and reg_type:
            if not reg_type == "representative":
                if len(ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH):
                    email_domain = email.split('@')[1]
                    matched = False
                    for ending in ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH:
                        if email_domain.endswith(ending):
                            matched = True
                            break
                    if not matched:
                        self._errors['email'] = self.error_class([_("""
                            Sorry! You have to have an email address ending with
                            %s to register as a volunteeer. If this is in error please email %s.
                            """ % (comma_or(ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH), SERVER_EMAIL)
                            )])
                        del cleaned_data["email"]

        # If registering as a representative, an organisation must be provided.
        if reg_type and organisation != None:
            if reg_type == "representative" and not len(organisation):
                self._errors['organisation'] = self.error_class(["If you are registering as an organisation representative you must enter the name of your organisation here."])
                del cleaned_data["organisation"]
            elif reg_type == "volunteer" and len(organisation):
                self._errors['organisation'] = self.error_class(["If you are registering as a volunteer you cannot enter the name of an organisation here."])
                del cleaned_data["organisation"]
            

        return cleaned_data

    first_name = forms.CharField()
    last_name = forms.CharField()
    reg_type = forms.ChoiceField(label="Registration Type", choices=(("volunteer", "Volunteer"), ("representative", "Organisation Representative"),))
    organisation = forms.CharField(label="Organisation", help_text="<b>If you are registering as an organisation representative</b>, please enter the name of your organisation above.", required=False)
    agree = forms.BooleanField(initial=True)

def comma_or(list_of_things):
    """Returns the list in the format: 'A', 'B' or 'C'"""
    # Copy
    list_of_things = list(list_of_things)

    def quote(s):
        return "'%s'" % s

    if len(list_of_things) == 0:
       return ""

    buf = quote(list_of_things.pop(0))

    while len(list_of_things) > 1:
        buf += ", " + quote(list_of_things.pop(0))

    if len(list_of_things) > 0:
        buf += " or " + quote(list_of_things.pop())

    return buf
