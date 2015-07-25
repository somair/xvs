from django.contrib import admin
from blogs.models import Entry

class blogadmin(admin.ModelAdmin):
	list_display = ('title', 'publisher')
	search_fields = ('title', 'publisher')

admin.site.register(Entry, blogadmin)