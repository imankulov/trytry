# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from trytry.core import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core-index'),
    url(r'^status/(?P<flow_name>\w*)/', views.get_status, name='core-status'),
    url(r'^(?P<flow_name>\w*)/', views.get_task, name='core-flow', ),
)
