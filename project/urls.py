# -*- encoding: utf-8 -*-

import os.path

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
# admin.autodiscover()

import coaching.admin

# Base
urlpatterns = patterns('email_auth.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
)

# Lost password
urlpatterns += patterns('django.contrib.auth.views',
    (r'^lostpw/$', 'password_reset'),
    (r'^lostpw/done/$', 'password_reset_done'),
    (r'^lostpw/confirm/(?P<uidb36>.*)/(?P<token>.*)$', 'password_reset_confirm'),
    (r'^lostpw/complete/$', 'password_reset_complete'),
)

# Applications
urlpatterns += patterns('',
    (r'^$', 'dashboard.views.dashboard'),
#    (r'^$', include(admin.site.urls)),
#    (r'^learning/', include('learning.urls')),
#    (r'^testing/', include('testing.urls')),
#    (r'^coaching/', include('coaching.urls')),
#    (r'^staff/coaching/utilisateur/create_logins/',
#        'coaching.views.create_logins'),
    (r'^staff/', include(admin.site.urls)),
    (r'^dashboard/$', 'dashboard.views.dashboard'),
    (r'^profile/$', 'coaching.views.profile'),
)

# Développement
if settings.SITE_ID==1:
    contents_root = os.path.join(settings.PROJECT_PATH, settings.CONTENTS_PREFIX)
    uploads_root = os.path.join(settings.PROJECT_PATH, settings.MEDIA_ROOT)
    urlpatterns += patterns('',
    (r'^static/contents/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': contents_root }),
    (r'^static/uploads/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': uploads_root }),
    (r'^static/media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': os.path.join(settings.PROJECT_PATH, 'static/media') }),
)
