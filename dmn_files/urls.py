# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('dmn_files.views',
    url(r'^elfinder2_connector/$', 'elfinder2_connector'),
    url(r'^files/$', 'elfinder'),
    url(r'^files_partial/$', 'elfinder_partial'),
)
