from django.conf import settings

# __all__ = []

# _DEFAULTS = {
#     'CAS_TICKET_EXPIRATION': 5, # In minutes
# }

settings.INSTALLED_APPS += (
    'dmn_local',
    'dmn.dmn_utils',
    'dmn.dmn_gallery',
    'dmn.dmn_files',
    'mptt',
    'annoying',
    'picklefield',
    'url_tools',
    'django_ajax',
    # 'markitup'
)

# for key, value in _DEFAULTS.iteritems():
#     try:
#         getattr(settings, key)
#     except AttributeError:
#         setattr(settings, key, value)
#     except ImportError:
#         pass
