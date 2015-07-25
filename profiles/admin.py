from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from models import *
from weekgrid import WeekgridField, WeekgridWidget
import settings

class VolunteerProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {
        WeekgridField: {'widget': WeekgridWidget},
        }
    search_fields = ['profile__user__first_name', 'profile__user__last_name']

class RepresentativeProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'get_email', 'organisation', 'job_title']
    search_fields = ['profile__user__first_name', 'profile__user__last_name']

class CourseInline(admin.TabularInline):
    model = Course
    extra = 15

class FacultyCourseAdmin(admin.ModelAdmin):
    inlines = [CourseInline,]
    list_display = ['__unicode__', 'course_count',]

class BaseProfileAdmin(admin.ModelAdmin):
    model = BaseProfile
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    search_fields = ['user__first_name', 'user__last_name']
    list_display = ['__unicode__', 'is_volunteer', 'is_representative']

admin.site.register(BaseProfile, BaseProfileAdmin)
admin.site.register(VolunteerProfile, VolunteerProfileAdmin)
admin.site.register(RepresentativeProfile, RepresentativeProfileAdmin)

if settings.FEATURE_HOW_DID_YOU_HEAR_OPTIONS:
    admin.site.register(HowDidYouHear)

if settings.FEATURE_COURSE_LIST:
    admin.site.register(Faculty, FacultyCourseAdmin)
elif settings.FEATURE_VOLUNTEER_SCHOOL:
    admin.site.register(Faculty)

if settings.FEATURE_SERVICE_LEVEL_AGREEMENTS:
    admin.site.register(ServiceLevelAgreement)

if settings.FEATURE_DEPARTMENTS:
    admin.site.register(Department)

if settings.FEATURE_AWARD:
    admin.site.register(AwardType)
    admin.site.register(Award)

