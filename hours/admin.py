from django.contrib import admin
from hours.models import *

class CommitmentAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'volunteer', 'organisation', 'started')

class EndorsementAdmin(admin.ModelAdmin):
	list_display = ('commitment', 'representative', 'created')

admin.site.register(Commitment, CommitmentAdmin)
admin.site.register(Endorsement, EndorsementAdmin)