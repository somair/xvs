from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^new/$', 'work_experience.views.new', name='we_new'),
)