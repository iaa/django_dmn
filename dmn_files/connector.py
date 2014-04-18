# -*- coding: utf-8 -*-
#orignal file https://github.com/Studio-42/elfinder-python/blob/master/connector.py
#license https://raw.github.com/Studio-42/elfinder-python/master/README.md
#changed by Alexandr Rakov 08-03-2012

import json
import elFinder
from pyramid.response import Response
from cgi import FieldStorage

#connector opts
_opts = {
	#'root' and url rewrite from ini file
	'root': '/tmp',
	'URL': 'http://0.0.0.0:6543/static/uploaded',
    'tmbPath': '/home/iaa/www/projects/pyrm/wupy/static/elfinder/uploaded/tmb',
	## other options
	'debug': True,
	'fileURL': True,  # if False: download files using connector, no direct urls to files
	# 'dirSize': True,
	# 'dotFiles': True,
	'fileMode': 0666,
	'dirMode': 0777,
	# 'uploadDeny': ['image', 'application'],
	# 'uploadAllow': ['image/png', 'image/jpeg'],
	# 'uploadOrder': ['deny', 'allow']
}

def connector(request):
    # init connector and pass options
    elf = elFinder.connector(_opts)

    # fetch only needed GET/POST parameters
    httpRequest = {}
    form=request.params
    for field in elf.httpAllowedParameters:
        if field in form:
            # Russian file names hack
            if field == 'name':
                httpRequest[field] = form.getone(field).encode('utf-8')

            elif field == 'targets[]':
                httpRequest[field] = form.getall(field)

            # handle CGI upload
            elif field == 'upload[]':
                upFiles = {}
                cgiUploadFiles = form.getall(field)
                for up in cgiUploadFiles:
                    if isinstance(up, FieldStorage):
                        upFiles[up.filename.encode('utf-8')] = up.file # pack dict(filename: filedescriptor)
                httpRequest[field] = upFiles
            else:
                httpRequest[field] = form.getone(field)

    # run connector with parameters
    status, header, response = elf.run(httpRequest)

    # get connector output and print it out

    result=Response(status=status)
    try:
        del header['Connection']
    except:
        pass
    result.headers=header

    if not response is None and status == 200:
        # send file
        if 'file' in response and isinstance(response['file'], file):
            result.body=response['file'].read()
            response['file'].close()

        # output json
        else:
            result.body=json.dumps(response)
    return result

def includeme(config):
    _opts['root']=config.registry.settings['elfinder_root']
    _opts['URL']=config.registry.settings['elfinder_url']
    _opts['tmbDir']=config.registry.settings['elfinder_tmb_path']
    _opts['tmbURL']=config.registry.settings['elfinder_tmb_url']

    config.add_route('connector', '/wupy/elfinder/connector')
    config.add_view(connector,route_name='connector')
