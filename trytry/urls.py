# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^', include('trytry.core.urls')),
    url(r'^simple_python/', include('trytry.simple_python.urls')),
)
if settings.DEBUG:
    admin.autodiscover()
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))
