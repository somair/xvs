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
	url(r'^admin/event/register/(?P<event_id>\d+)/delete/$', 'training.views.delete_event', name='delete_event'),
	url(r'^admin/event/register/(?P<event_id>\d+)/contact/$', 'training.views.non_attendee_contact', name='non_attendee_contact'),
	url(r'^admin/event/register/(?P<event_id>\d+)/confirm/(?P<attendee_id>\d+)/$', 'training.views.confirm_attendance', name='confirm_attendance'),
	url(r'^admin/event/register/(?P<event_id>\d+)/remove/(?P<attendee_id>\d+)/$', 'training.views.remove_attendance', name='remove_attendance'),

	url(r'^report/$', 'training.views.training_report', name='training_report'),

)