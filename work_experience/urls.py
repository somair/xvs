from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^dashboard/$', 'work_experience.views.work_experience', name='we_dashboard'),
	url(r'^delete/(?P<we_id>\d+)$', 'work_experience.views.work_experience_delete', name='we_delete'),

)