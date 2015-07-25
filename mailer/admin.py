from django.contrib import admin
from mailer.models import *

class MailoutAdmin(admin.ModelAdmin):
	list_display = ('id', 'subject', 'created', 'updated', 'sent')


admin.site.register(Mailout, MailoutAdmin)