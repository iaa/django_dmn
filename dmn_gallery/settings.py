# -*- coding: utf-8 -*-

import os
from django.conf import settings

DMN_GALLERY = os.path.join(settings.MEDIA_ROOT, 'dmn_gallery')
DMN_GALLERY_URL = os.path.join(settings.MEDIA_URL, 'dmn_gallery')
UPLOAD_TMP = os.path.join(settings.MEDIA_ROOT, 'dmn_gallery', 'tmp')
UPLOAD_GALLERY = os.path.join(settings.MEDIA_ROOT, 'dmn_gallery', 'gallery')
UPLOAD_GALLERY_URL = os.path.join(settings.MEDIA_URL, 'dmn_gallery', 'gallery')
TMB = [128, 128]
