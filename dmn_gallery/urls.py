# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('dmn_gallery.views',
    url(r'^upload_gallery/$', 'upload_gallery', name='upload_gallery'),
    url(r'^upload_gallery_details/$', 'upload_gallery_details', name='upload_gallery_details'),
    url(r'^aj_delete_hide_img/$', 'aj_delete_hide_img', name='aj_delete_hide_img'),
)
