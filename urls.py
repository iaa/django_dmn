# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
#from django.views.generic.simple import redirect_to
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.auth.views import login, logout
from dmn.views import Create, Update
from dmn.views import (List,
                       Tree,
                       CatTree,
                       UserCreate,
                       UserUpdate,
                       Destroy,
                       GroupList,
                       GroupCreate,
                       GroupUpdate,
                       GroupDestroy,
                       PermisionList,
                       PermisionCreate,
                       PermisionUpdate,
                       PermisionDestroy)

urlpatterns = patterns('dmn.views',
    url(r'^', include('dmn_local.urls')),
    url(r'^$', 'index', name='index'),
    url(r'^user/create/$', RedirectView.as_view(permanent=False, url='/dmn/user_create/', query_string=True)),
    url(r'^user/update/(?P<id>\d+)/$', RedirectView.as_view(permanent=False, url='/dmn/user_update/%(id)s/', query_string=True)),
    url(r'^group/create/$', GroupCreate.as_view(), name='group_create'),
    url(r'^group/update/(?P<id>\d+)/$', GroupUpdate.as_view(), name='group_create'),
    url(r'^permission/create/$', PermisionCreate.as_view(), name='permission_create'),
    url(r'^permission/update/(?P<id>\d+)/$', PermisionUpdate.as_view(), name='permission_create'),
    url(r'^(?P<model>\w+)/create/$', Create.as_view(), name='dmn_create'),
    url(r'^(?P<model>\w+)/update/(?P<id>\d+)/$', Update.as_view(), name='dmn_update'),
    url(r'^group/destroy/(?P<id>\d+)/$', GroupDestroy.as_view(), name='group_destroy'),
    url(r'^permission/destroy/(?P<id>\d+)/$', PermisionDestroy.as_view(), name='permission_destroy'),
    url(r'^(?P<model>\w+)/destroy/(?P<id>\d+)/$', Destroy.as_view(), name='destroy'),
    url(r'^group/destroymore/(.*)$', GroupDestroy.as_view(), name='group_destroy'),
    url(r'^permission/destroymore/(.*)$', PermisionDestroy.as_view(), name='permission_destroy'),
    url(r'^(?P<model>\w+)/destroymore/(.*)$', Destroy.as_view(), name='destroy'),
    url(r'^(?P<model>\w+)/toggle/(?P<attr>\w+)/(?P<id>\d+)$', 'toggle'),
    url(r'^(?P<model>\w+)/fastedit/$', 'fastedit'),
    # url(r'^aj_del_attach/$', 'aj_del_attach', name='aj_del_attach'),
    # url(r'^aj_sort_grid/$', 'aj_sort_grid', name='aj_sort_grid'),
    url(r'^(?P<model>\w+)/tree/$', Tree.as_view(), name='tree'),
    url(r'^(?P<model>\w+)/cat_tree/$', CatTree.as_view(), name='cat_tree'),
    url(r'^tree_change_pid/(?P<model>\w+)/(?P<id>\d+)/(?P<pid>\d+)/(?P<position>\w+)$', 'tree_change_pid', name='tree_change_pid'),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'next_page': '/dmn/accounts/login/?next=/dmn/'}),
    # url(r'^ajax_get_verbose_name/$', 'ajax_get_verbose_name', name='ajax_get_verbose_name'),
    # url(r'^ajax_checkbox_options/$', 'ajax_checkbox_options', name='ajax_checkbox_options'),
    url(r'^yamail/$', 'yamail',  name='yamail'),
    # url(r'^shop_param_default/$', 'shop_param_default',  name='shop_param_default'),
    # url(r'^markitup/', include('markitup.urls')),
    # url(r'^help/', 'help',  name='help'),
    url(r'^group/list/$', GroupList.as_view(), name='group_list'),
    url(r'^permission/list/$', PermisionList.as_view(), name='permission_list'),
    url(r'^(?P<model>\w+)/list/$', List.as_view(), name='list'),
    url(r'^user_create/$', UserCreate.as_view(), name='user_create'),
    url(r'^user_update/(?P<id>\d+)/$', UserUpdate.as_view(), name='user_create'),

)

if 'dmn_gallery' in settings.INSTALLED_APPS:
    urlpatterns += patterns('dmn_gallery.views',
        url(r'^', include('dmn_gallery.urls')),
    )

if 'dmn_files' in settings.INSTALLED_APPS:
    urlpatterns += patterns('dmn_files.views',
        url(r'^', include('dmn_files.urls')),
    )
