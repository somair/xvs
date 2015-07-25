from django.conf.urls.defaults import *
import settings

from decorators import staff_required

import positions.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^notes/new$', 'notes.views.new'),
    (r'^notes/delete$', 'notes.views.delete'),

    (r'^profiles/update$', 'profiles.views.update'),
    (r'^profiles/communication$', 'profiles.views.communication'),
    url(r'^profiles/volunteers/$', 'profiles.views.volunteers', {'filter': 'all'}, name='volunteers-list-all'),
    url(r'^profiles/volunteers/uncommitted$', 'profiles.views.volunteers', {'filter': 'uncommitted'}, name='volunteers-list-uncommitted'),
    url(r'^profiles/volunteers/inactive$', 'profiles.views.volunteers', {'filter': 'inactive'}, name='volunteers-list-inactive'),
    url(r'^profiles/volunteers/deactivated$', 'profiles.views.volunteers', {'filter': 'deactivated'}, name='volunteers-list-deactivated'),
    url(r'^profiles/volunteers/action/recommend/(?P<position_id>\d+)$', 'profiles.views.volunteers', {'filter': 'all', 'action': 'recommend'}, name='volunteers-list-action-recommend'),
    url(r'^profiles/volunteers/action/mailout/(?P<organisation_id>\d*)$', 'profiles.views.volunteers', {'filter': 'all', 'action': 'mailout'}, name='volunteers-list-action-mailout'),
    url(r'^profiles/representatives/$', 'profiles.views.representatives', {'filter': 'all'}, name='representatives-list-all'),
    url(r'^profiles/representatives/action/mailout$', 'profiles.views.representatives', {'filter': 'all', 'action': 'mailout'}, name='representatives-list-action-mailout'),
    url(r'^profiles/marketing/$', 'profiles.views.marketing', {'filter': 'all'}, name='marketing-report-all'),
    url(r'^profiles/bulk_deactivate/$', 'profiles.views.bulk_deactivate'),
    (r'^profiles/(?P<user_id>\d+)/$', 'profiles.views.profile'),
    (r'^profiles/(?P<user_id>\d+)/photo$', 'profiles.views.volunteer_photo'),
    (r'^profiles/(?P<user_id>\d+)/thumb$', 'profiles.views.volunteer_photo_thumb'),
    (   r'^profiles/(?P<user_id>\d+)/hours$', 'hours.views.volunteer_hours'),
    (   r'^profiles/(?P<user_id>\d+)/offers$', 'profiles.views.offers'),
    (   r'^profiles/(?P<user_id>\d+)/approve$', 'profiles.views.approve'),
    (   r'^profiles/(?P<user_id>\d+)/reference$', 'profiles.views.serve_reference_file'),
    (   r'^profiles/(?P<user_id>\d+)/cv$', 'profiles.views.serve_cv'),

    (r'^positions/new$', 'positions.views.new'),
    url(r'^positions/$', positions.views.all, {'filter': 'all'}, name='positions-list-all'),
    url(r'^positions/calendar$', positions.views.calendar, name="positions-calendar"),
    url(r'^positions/no-offers$', staff_required(positions.views.all), {'filter': 'no-offers'}, name='positions-list-no-offers'),
    url(r'^positions/five-pending$', staff_required(positions.views.all), {'filter': 'five-pending'}, name='positions-list-five-pending'),
    (r'^positions/match$', 'positions.views.match'),
    (   r'^positions/(?P<position_id>\d+)/apply$', 'positions.views.apply'),
    (   r'^positions/(?P<position_id>\d+)/edit$', 'positions.views.edit'),
    url(r'^positions/(?P<position_id>\d+)/', 'positions.views.position', name='position-detail' ),
    (r'^positions/feed/$', positions.views.LatestPositionsFeed()),

    url(r'^mailouts/(?P<organisation_id>\d*)$', 'mailer.views.mailouts', name='mailouts-list-all'),
    url(r'^mailouts/new$', 'mailer.views.new', name='mailouts-new'),
    url(r'^mailouts/(?P<mailout_id>\d+)/$', 'mailer.views.mailout', name='mailout-detail'),
    url(r'^mailouts/users/$', 'mailer.views.user_autocomplete', name='mailout-user-autocomplete'),
    url(r'^mailouts/copy/(?P<mailout_id>\d+)/$', 'mailer.views.copy', name='mailout-copy'),

    (r'^organisations/$', 'positions.views.organisations'),
    (r'^organisations/(?P<organisation_id>\d+)/$', 'positions.views.organisation'),
    (r'^organisations/(?P<organisation_id>\d+)/photo$', 'positions.views.organisation_primary_image'),
    (r'^organisations/(?P<organisation_id>\d+)/volunteers$', 'hours.views.organisation_volunteers'),
    url(r'^organisations/autocomplete$', 'positions.views.organisations_autocomplete', name="organisations-autocomplete"),

    (r'^reports/inactive_volunteers$', 'reports.views.inactive_volunteers'),
    url(r'^reports/sla/all$', 'reports.views.sla_check', {'filter': 'all'}, name="sla-report-all"),
    url(r'^reports/sla/$', 'reports.views.sla_check', {'filter': 'recent'}, name="sla-report-recent"),
    (r'^reports/activity$', 'reports.views.activity'),
    (r'^reports/time_records$', 'reports.views.time_records'),
    url(r'^reports/user-breakdown/$', 'reports.views.user_breakdown', {}, name='user-breakdown'),

    (r'^offers/recent$', 'offers.views.recent'),
    (r'^offers/my$', 'offers.views.representative_offers'),
    (r'^offers/(?P<offer_id>\d+)/$', 'offers.views.offer'),

    (r'^actions/do$', 'actions.views.do'),

    (r'^hours/commitments/(?P<commitment_id>\d+)/$', 'hours.views.commitment'),
    (r'^hours/commitments/(?P<commitment_id>\d+)/set_finish_date$', 'hours.views.set_finish_date'),
    (r'^hours/commitments/(?P<commitment_id>\d+)/clear_finish_date$', 'hours.views.clear_finish_date'),
    (r'^hours/review$', 'hours.views.review'),
    (r'^hours/review/(?P<organisation_id>\d+)$', 'hours.views.review'),
    (r'^hours/delete$', 'hours.views.delete'),
    (r'^hours/mark_record$', 'hours.views.mark_record'),
    (r'^hours/add_volunteer$', 'hours.views.add_volunteer'),

    (r'^(?P<page_name>[a-z]+)$', 'pages.views.render_page'),
    (r'^$', 'pages.views.render_page', { 'page_name': 'index' }),

    (r'^accounts/', include('registration.backends.default.urls')),
)

if settings.FEATURE_VOLUNTEER_BLOGS or settings.FEATURE_ORGANISATION_BLOGS or settings.FEATURE_SITE_BLOG:
    urlpatterns += patterns('',
        (r'^blogs/$', 'blogs.views.myblog'),
        (r'^blogs/all$', 'blogs.views.bloggers'),
        (r'^blogs/(?P<user_id>\d+)/$', 'blogs.views.blogview'),
        (r'^blogs/(?P<user_id>\d+)/(?P<entry_id>\d+)$', 'blogs.views.entryview'),
        (r'^blogs/new', 'blogs.views.newentry'),
        (r'^blogs/edit/(?P<entry_id>\d+)$', 'blogs.views.editentry'),
        (r'^blogs/delete/(?P<entry_id>\d+)$', 'blogs.views.deleteentry'),
        (r'^blogs/publish/(?P<entry_id>\d+)$', 'blogs.views.publishentry'),
        (r'^blogs/admin', 'blogs.views.blogadmin'),
    )


if settings.FEATURE_CMS:
    urlpatterns +=  patterns('',
        (r'^cms/$', 'cms.views.cms'),
        (r'^cms/(\d+)/$', 'cms.views.edit'),
        (r'^cms/pages/$', 'cms.views.pages'),
        (r'^cms/pages/(\d+)/$', 'cms.views.pageview'),
        (r'^cms/delete/(\d+)/$', 'cms.views.delete'),
        (r'^cms/order/$', 'cms.views.order'),
        (r'^cms/up/(\d+)/(\d+)/$', 'cms.views.up'),
        (r'^cms/down/(\d+)/(\d+)/$', 'cms.views.down'),
        (r'^site/$', 'cms.views.site'),
        (r'^site/(\d+)/$', 'cms.views.siteview'),
        (r'^site/admin/$', 'cms.views.siteadmin'),
        (r'^cms/publish/(\d+)/$', 'cms.views.publish'),
    )

if settings.FEATURE_ENDORSEMENT:
    urlpatterns +=  patterns('',
        (r'^hours/endorsement/(?P<commitment_id>\d+)/$', 'hours.views.add_endorsement'),
    )

if settings.FEATURE_AWARD:
    urlpatterns +=  patterns('',
        (r'^reports/awards$', 'reports.views.awards'),
    )

if settings.FEATURE_LOGIN_AS:
    urlpatterns +=  patterns('',
        url(r'^profiles/loginas/(?P<user_id>\d+)/$', 'profiles.views.login_as_user', name='login_as_user' ),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        )
