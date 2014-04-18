from django.conf import settings

settings.INSTALLED_APPS += (
    'dmn_local',
    'dmn.dmn_utils',
    'dmn.dmn_gallery',
    'dmn.dmn_files'
)

_REQUIREMENTS_INSTALLED_APPS = (
    'mptt',
    'annoying',
    'picklefield',
    'url_tools',
    'django_ajax',
    # 'markitup'
)

_REQUIREMENTS_TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages'
)

for k in _REQUIREMENTS_INSTALLED_APPS:
    if k not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += (k, )

for k in _REQUIREMENTS_TEMPLATE_CONTEXT_PROCESSORS:
    if k not in settings.TEMPLATE_CONTEXT_PROCESSORS:
        settings.TEMPLATE_CONTEXT_PROCESSORS += (k, )
