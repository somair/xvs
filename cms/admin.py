from django.contrib import admin
from cms.models import Page

class PageAdmin(admin.ModelAdmin):
	search_fields = ('page_name', 'link')

admin.site.register(Page, PageAdmin)