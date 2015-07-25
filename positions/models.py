from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from weekgrid import WeekgridField
from south.modelsinspector import add_introspection_rules
from validators import validate_numerals

import datetime
import settings
from lxml.html.clean import clean_html

import offers.models
import hours.models

fs = FileSystemStorage(location=settings.UPLOAD_ROOT)

# Explain WeekgridFields to south
add_introspection_rules([], ["WeekgridField"])


# These are the columns that staff can choose to show or not show when displaying volunteers.
POSITION_COLUMN_CHOICES = (
    ("type", "Type"),
    ("organisation", "Organisation"),
    ("summary", "Summary"),
    ("created", "Created"),
)
POSITION_COLUMN_CHOICES_DEFAULT = ["type", "organisation", "summary"]


class OrganisationCategory(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "organisation categories"


class Organisation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    category = models.ForeignKey(OrganisationCategory, blank=True, null=True)
    department = models.ForeignKey("profiles.Department", blank=True, null=True)
    name = models.CharField(max_length=127)
    charity_number = models.CharField(max_length=15, blank=True)
    purpose = models.TextField(blank=True)
    location = models.TextField("Post address", blank=True)
    website = models.URLField(null=True, blank=True)
    directions = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=31, 
        blank=True, 
        default="",
        validators=[validate_numerals] if settings.FEATURE_NUMERAL_PHONE_NUMBERS_ONLY else []
        )
    description = models.TextField(blank=True, default="")
    volunteer_policy = models.TextField(blank=True, default="")
    primary_image = models.ImageField(null=True, blank=True, storage=fs, upload_to="orgprimaryimages")

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('positions.views.organisation', (self.id,))

    def current_positions(self):
        return self.positions.filter(approved=True, active=True)

    def clean_description(self):
        return clean_html(self.description)

    def old_positions(self):
        return self.positions.filter(approved=True, active=False)

    def unapproved_positions(self):
        return self.positions.filter(approved=False)

    def all_applications(self):
        return offers.models.Offer.objects.filter(position__organisation=self)

    def applications_received(self):
        return self.all_applications().filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            )

    def applications_accepted(self):
        return self.all_applications().filter(
            time_representative_accepted__isnull=False,
            )

    def applications_rejected(self):
        return self.all_applications().filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            representative__isnull=False,
            time_withdrawn__isnull=False,
            )

    def applications_withdrawn(self):
        return self.all_applications().filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            representative__isnull=True,
            time_withdrawn__isnull=False,
            )

    def applications_in_progress(self):
        return self.all_applications().filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            representative__isnull=True,
            time_withdrawn__isnull=True
            )

    def hour_records_logged(self):
        return hours.models.TimeRecord.objects.filter(organisation=self)

    def hour_records_validated(self):
        return self.hour_records_logged().filter(reviewed_by__isnull=False)

    def hour_records_not_validated(self):
        return self.hour_records_logged().filter(reviewed_by__isnull=True)




class Skill(models.Model):
    name = models.CharField(max_length=31)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

expenses_paid_choices = (
    (True, "Travel expenses will be reimbursed"),
    (False, "We are unable to reimburse travel expenses"),
    )

class PositionCategory(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "position categories"

class Position(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    organisation = models.ForeignKey(Organisation, related_name='positions')
    category = models.ManyToManyField(PositionCategory, blank=True, null=True)
    representative = models.ForeignKey(User, related_name='positions')
    name = models.CharField(max_length=63)
    summary = models.CharField(max_length=140)
    description = models.TextField()
    location = models.TextField()
    latlong = models.CharField(max_length=32, null=True, blank=True)
    training_provided = models.BooleanField(default=False)
    training_details = models.TextField(null=True, blank=True)
    travel_expenses = models.NullBooleanField(default=False, choices=expenses_paid_choices)
    skills_gained = models.ManyToManyField(Skill)
    spec_essential = models.CharField(max_length=140)
    spec_desirable = models.CharField(max_length=140)
    number_of_volunteers = models.CharField(max_length=140, null=True, blank=True)

    keywords = models.CharField(max_length=64, blank=True)
    
    oneoff = models.BooleanField(default=False)

    # If not one-off...
    hours = WeekgridField()
    
    # If one-off...
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    
    # For weekly opportunities, hours per week
    # For one-offs, total number of hours expected
    hour_count = models.IntegerField(null=True, blank=False)

    # Marks a position as eligible for Plus awards
    plus_eligible = models.BooleanField(default=False)
    
    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def offerers(self):
        """Returns a list of every user who has offered or been recommended for this position."""
        return User.objects.filter(offers_made__position=self)

    def pending_offerers(self):
        """Returns a list of users who currently have an offer open for this position. These users are not allowed to apply."""
        return User.objects.filter(offers_made__position=self, offers_made__time_representative_accepted__isnull=True, offers_made__time_withdrawn__isnull=True)

    def successful_offerers(self):
        """Returns a list of users who have a successful offer for the position. These users are not allowed to apply."""
        return User.objects.filter(offers_made__position=self, offers_made__time_representative_accepted__isnull=False)

    def __unicode__(self):
        return "%s at %s" % (self.name, self.organisation.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('positions.views.position', (self.id,))

    
    def offers_in_progress(self):
        """All offers that haven't been started or withdrawn yet"""
        return self.offer_set.filter(
            time_confirmed_started__isnull=True,
            time_withdrawn__isnull=True,
        )

    def offers_in_progress_volunteer_offered(self):
        """All offers in progress, minus recommendations that the volunteer
        hasn't agreed to yet."""
        return self.offers_in_progress().filter(
            time_volunteer_accepted__isnull=False
        )

    def offers_completed(self):
        offers = self.offer_set.filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            time_confirmed_started__isnull=False,
            )
        return offers
