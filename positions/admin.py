from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from models import *
from weekgrid import WeekgridField, WeekgridWidget
import settings

class PositionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        WeekgridField: {'widget': WeekgridWidget},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
        }
    list_display = ['__unicode__', 'organisation']
    search_fields = ['name']

class PositionCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class OrganisationAdmin(admin.ModelAdmin):
	exclude = None if settings.FEATURE_ORGANISATION_CATEGORIES else ('category',)
	search_fields = ['name']   

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PositionCategory, PositionCategoryAdmin)
admin.site.register(Skill)

if settings.FEATURE_ORGANISATION_CATEGORIES:
	admin.site.register(OrganisationCategory)