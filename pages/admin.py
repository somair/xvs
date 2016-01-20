from django.contrib import admin
from pages import models

class LinkAdmin(admin.ModelAdmin):
	list_display = ('title', 'href')
	search_fields = ('title', 'href')

admin.site.register(models.Link, LinkAdmin)