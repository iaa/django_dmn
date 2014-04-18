# -*- coding: utf-8 -*-
import os
from django.shortcuts import render
from django.conf import settings
from dmn_files.elFinder import connector as elfConnector
from json import JSONEncoder
from dmn_files.extras import upload_file_to, find_dir
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from dmn_utils import views as utils_views
from dmn import const
from django.http import HttpResponse


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
@csrf_exempt
def elfinder2_connector(request):
    elf_opts = {'root': os.path.join(settings.MEDIA_ROOT, 'dmn/elf'),
                'URL': os.path.join(settings.MEDIA_URL, 'dmn/elf'),
                'rootAlias': 'Файлы',
                'fileURL': True,
                'dotFiles': True,
                'dirSize': True,
                'fileMode': 0644,
                'dirMode': 0777,
                'imgLib': 'auto',
                'tmbDir': os.path.join(settings.MEDIA_ROOT, 'dmn/elf/.tmb/'),
                'tmbAtOnce': 5,
                'tmbSize': 48,
                'uploadMaxSize': 128,
                'uploadAllow': [],
                'uploadDeny': [],
                'uploadOrder': ['allow', 'deny'],
                'defaults': {'read': True, 'write': True, 'rm': True},
                'perms': {},
                'archiveMimes': {},
                'archivers': {},
                'disabled': [],
                'iexclude': ['.tmb'],
                'debug': False}

    output = None
    elf = elfConnector(elf_opts)

    if request.method == 'GET':
        http_status, http_header, http_response = elf.run(request.GET)
        output = JSONEncoder().encode(http_response)

    if request.method == 'POST':
        cur_cmd = request.POST.get('cmd', False)

        if cur_cmd and cur_cmd == 'upload':
            cur_dir = request.POST.get('current', False)
            files = request.FILES.lists()
            path = find_dir(cur_dir, elf_opts['root'])
            upload_file_to(files, path, elf_opts['uploadMaxSize'])
            http_status, http_header, http_response = elf.run({u'target': cur_dir})
            output = JSONEncoder().encode(http_response)
        else:
            http_status, http_header, http_response = elf.run(request.POST)
            output = JSONEncoder().encode(http_response)
    return HttpResponse(output)


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def elfinder(request):
    return render(request, 'dmn_files/elfinder.html')


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def elfinder_partial(request):
    return render(request, 'dmn_files/elfinder_partial.html')
