from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from weekgrid import WeekgridField
from positions.models import Organisation, PositionCategory
from offers.models import Offer

from validators import validate_numerals

import settings

fs = FileSystemStorage(location=settings.UPLOAD_ROOT)


class ServiceLevelAgreement(models.Model):
    statement = models.TextField(help_text="This can be in the form of a question ('Does your organisation have a health and safety policy?') or an assertion ('Our organisation has a health and safety policy')")
    order = models.IntegerField(default=1)
    preferred_answer = models.BooleanField(default=True, choices=(
        (True, "The representative should answer 'Yes'"),
        (False, "The representative should answer 'No'"),
        ), help_text="When you review the representative's answers, we will highlight answers that aren't preferred so that they are easier to spot.")

    def __unicode__(self):
        return self.statement

    def field_name(self):
        return "sla_%d" % self.id

    class Meta:
        ordering = ('order',)


class Department(models.Model):
    """Registering representatives can request that their organisation be associated with a given department."""
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        

class BaseProfile(models.Model):
    archived = models.BooleanField(default=False)

    user = models.OneToOneField(User)
    is_volunteer = models.BooleanField(default=False)
    is_representative = models.BooleanField(default=False)
    slas = models.ManyToManyField(ServiceLevelAgreement, verbose_name="SLA responses", blank=True)
    department = models.ForeignKey(Department, null=True, blank=True)
    communication = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def try_get_representative_profile(self):
        try:
            return self.representativeprofile
        except RepresentativeProfile.DoesNotExist:
            return None

    def try_get_volunteer_profile(self):
        try:
            return self.volunteerprofile
        except VolunteerProfile.DoesNotExist:
            return None

    def offers_offered(self):
        offers = Offer.objects.filter(
            volunteer=self.user,
            time_volunteer_accepted__isnull=False,
            )
        return offers

    def offers_in_progress(self):
        """All offers that haven't been started or withdrawn yet"""
        return Offer.objects.filter(
            volunteer=self.user,
            time_confirmed_started__isnull=True,
            time_withdrawn__isnull=True,
        )

    def offers_withdrawn(self):
        """Every offer that is not in progress"""
        return Offer.objects.filter(
            volunteer=self.user,
            time_withdrawn__isnull=False
        )

    def offers_completed(self):
        offers = Offer.objects.filter(
            volunteer=self.user, 
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=False,
            time_confirmed_started__isnull=False,
            )
        return offers

    def total_hours(self):
        trs = self.user.timerecord_set.aggregate(Sum('hours'), Sum('minutes'))
        trs['hours__sum'] = trs['hours__sum'] or 0
        trs['minutes__sum'] = trs['minutes__sum'] or 0
        return trs['hours__sum'] + trs['minutes__sum']/60.

    def total_confirmed_hours(self):
        trs = self.user.timerecord_set.filter(confirmed=True).aggregate(Sum('hours'), Sum('minutes'))
        trs['hours__sum'] = trs['hours__sum'] or 0
        trs['minutes__sum'] = trs['minutes__sum'] or 0
        return trs['hours__sum'] + trs['minutes__sum']/60.


#TODO: Generate with range so that XVS can still be used post-2024.
YEAR_CHOICES = (
    (2009, "2009"),
    (2010, "2010"),
    (2011, "2011"),
    (2012, "2012"),
    (2013, "2013"),
    (2014, "2014"),
    (2015, "2015"),
    (2016, "2016"),
    (2017, "2017"),
    (2018, "2018"),
    (2019, "2019"),
    (2020, "2020"),
    (2021, "2021"),
    (2022, "2022"),
    (2023, "2023"),
    (2024, "2024"),
)

GRAD_CHOICES = settings.GRAD_CHOICES
INTERNATIONAL_CHOICES = settings.INTERNATIONAL_CHOICES

GENDER_CHOICES = (
    ("U", "Unspecified"),
    ("M", "Male"),
    ("F", "Female"),
)

# These are the columns that staff can choose to show or not show when displaying volunteers.
VOLUNTEER_COLUMN_CHOICES = (
    ("course", "Course"),
    ("registered", "Registered"),
    ("grad_year", "Grad. year"),
    ("offers", "Offers"),
    ("last_accepted", "Last accepted"),
    ("hours_logged", "Hours logged"),
)
VOLUNTEER_COLUMN_CHOICES_DEFAULT = ["course", "registered", "offers"]

class VolunteerProfile(models.Model):
    profile = models.OneToOneField(BaseProfile)

    # We use the course field to identify if the volunteer
    # is "available", so this field should NEVER be allowed
    # to be null.
    course = models.CharField(max_length=63)
    school = models.CharField(max_length=127, blank=True, default="")
    contact_email = models.EmailField(max_length=127, blank=True, null=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    postgrad = models.NullBooleanField(default=False, choices=GRAD_CHOICES)
    international = models.CharField(default='H', max_length=1, choices=INTERNATIONAL_CHOICES)
    phone_number = models.CharField(max_length=31, 
        validators=[validate_numerals] if settings.FEATURE_NUMERAL_PHONE_NUMBERS_ONLY else []
        )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)

    photo = models.ImageField(null=True, blank=True, storage=fs, upload_to="volunteerphotos")

    bio = models.TextField(null=True, blank=False)
    hours = WeekgridField()
    
    referrer = models.CharField(max_length=255, null=True, blank=True)

    referencefile = models.FileField(storage=fs, upload_to="referencefiles", null=True, blank=True)
    cv = models.FileField(storage=fs, upload_to="cvs", null=True, blank=True)

    # These fields are only allowed to be blank if the features are not enabled.
    address = models.TextField(null=True, blank=not settings.FEATURE_VOLUNTEER_ADDRESS)
    student_id = models.CharField(max_length=31, null=True, blank=not settings.FEATURE_VOLUNTEER_STUDENT_ID)

    categories = models.ManyToManyField(PositionCategory, blank=True, null=True)

    def __unicode__(self):
        return self.profile.user.get_full_name()

    def school_or_faculty(self):
        # Some instances allow students to set a school directly.
        if settings.FEATURE_VOLUNTEER_SCHOOL:
            return self.school

        # Some instances make students choose their course from a list,
        # in which case they have an implicity faculty.
        if settings.FEATURE_COURSE_LIST:
            try:
                course = Course.objects.get(name=self.course)
                return course.faculty.name
            except Course.DoesNotExist:
                return None

        return None

    def save(self, *args, **kwargs):
        if settings.FEATURE_COURSE_LIST:
            # Set the faculty if possible.
            courses = Course.objects.filter(name=self.course)
            if len(courses) > 0:
                self.school = courses[0].faculty.name
        # Actually save.
        super(VolunteerProfile, self).save(*args, **kwargs)


class RepresentativeProfile(models.Model):
    profile = models.OneToOneField(BaseProfile)
    organisation = models.ForeignKey(Organisation)
    job_title = models.CharField(max_length=63)

    def __unicode__(self):
        return self.profile.user.get_full_name()

    def get_email(self):
        return self.profile.user.email
    get_email.short_description = 'Email'


class HowDidYouHear(models.Model):
    how = models.CharField(max_length=255, verbose_name="I heard about the Volunteering site...")

    class Meta:
        verbose_name = "\"How did you hear...?\" option"

    def __unicode__(self):
        return self.how

class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name="faculty name")

    def __unicode__(self):
        return self.name

    def course_count(self):
        return self.course_set.count()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "faculties"

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="course name", unique=True)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class AwardType(models.Model):
    name = models.CharField(max_length=50)
    hours_required = models.IntegerField()
    plus = models.BooleanField(default=False)

    training_required = models.ManyToManyField('training.Training', blank=True, null=True)

    def __unicode__(self):
        return self.name

class Award(models.Model):
    award = models.ForeignKey(AwardType)
    user = models.ForeignKey(User)
    date_awarded = models.DateField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.award.name, self.user.username)
