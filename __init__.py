from django.conf import settings

__all__ = []

_DEFAULTS = {
    'CAS_TICKET_EXPIRATION': 5, # In minutes
}

settings.INSTALLED_APPS += (
    'dmn',
    'dmn_local',
    'dmn_utils',
    'dmn_gallery',
    'dmn_files',
    'mptt',
    'annoying',
    'picklefield',
    'url_tools',
    'django_ajax',
    # 'markitup'
)

for key, value in _DEFAULTS.iteritems():
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    except ImportError:
        pass