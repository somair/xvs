from django.contrib import admin
from training.models import *

class TrainingAdmin(admin.ModelAdmin):
	search_fields = ('title',)

admin.site.register(Training, TrainingAdmin)
admin.site.register(Event,)
admin.site.register(Attendee,)