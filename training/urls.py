from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

	url(r'^$', 'training.views.index', name='training_index'),
	url(r'^event/(?P<event_id>\d+)/$', 'training.views.view', name='training_view'),
	url(r'^event/(?P<event_id>\d+)/attend/$', 'training.views.attend', name='training_attend'),
	url(r'^event/(?P<event_id>\d+)/withdraw/$', 'training.views.withdraw', name='training_withdraw'),

	url(r'^admin/$', 'training.views.admin', name='training_admin'),
	
	url(r'^admin/training/new/$', 'training.views.new_training', name='new_training'),
	url(r'^admin/training/edit/(?P<training_id>\d+)/$', 'training.views.new_training', name='edit_training'),

	url(r'^admin/event/new/$', 'training.views.new_event', name='new_event'),
	url(r'^admin/event/edit/(?P<event_id>\d+)/$', 'training.views.new_event', name='edit_event'),
	url(r'^admin/event/register/(?P<event_id>\d+)/$', 'training.views.attendance_register', name='event_register'),

)