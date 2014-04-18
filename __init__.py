from django.conf import settings

settings.INSTALLED_APPS += (
    'dmn_local',
    'dmn.dmn_utils',
    'dmn.dmn_gallery',
    'dmn.dmn_files'
)

_REQUIREMENTS = (
    'mptt',
    'annoying',
    'picklefield',
    'url_tools',
    'django_ajax',
    # 'markitup'
)

for k in _REQUIREMENTS:
    if k not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += (k, )

print settings.INSTALLED_APPS
