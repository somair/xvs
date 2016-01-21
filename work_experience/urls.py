from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', 'work_experience.views.work_experience', name='work_experience'),
	url(r'^delete/(?P<we_id>\d+)$', 'work_experience.views.work_experience_delete', name='work_experience_delete'),
	url(r'^confirm/(?P<confirmation_code>[\w-]+)$', 'work_experience.views.work_experience_confirm', name='work_experience_confirm'),

	url(r'^report/$', 'work_experience.views.report', name='work_experience_report'),


)