# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('trytry.simple_python.views',
    url(r'^$', 'simple_python_get_task', name=u'simple-python-get-task'),
)
