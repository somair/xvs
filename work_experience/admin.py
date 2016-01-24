from django.contrib import admin
from work_experience.models import *

class WorkExperienceAdmin(admin.ModelAdmin):
	search_fields = ('volunteer__profile__user__first_name','volunteer__profile__user__last_name')

admin.site.register(WorkExperience, WorkExperienceAdmin)

