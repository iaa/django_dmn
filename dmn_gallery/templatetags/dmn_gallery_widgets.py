# -*- coding: utf-8 -*-

import os
import shutil
from django import template
from dmn import const
# from dmn_utils.models import getModelByName
from dmn_utils.spizz.pytils.translit import slugify
from dmn_gallery.models import DmnGalleryMixin, DmnGallery, DmnGalleryDetail
from django.forms.models import modelform_factory
# from dmn_utils.forms import Dform
# from django.utils.encoding import smart_str
from django.forms.widgets import HiddenInput

register = template.Library()


@register.inclusion_tag('dmn_gallery/dmn_gallery.html')
def dmn_gallery(model, form_class, id=None):
    render_gallery = None
    photos = []
    if isinstance(model, DmnGalleryMixin) or ('photos' in model._meta.get_all_field_names()):
        if os.path.exists(const.PATH_UPLOAD_GALLERY_TMP):
            shutil.rmtree(const.PATH_UPLOAD_GALLERY_TMP)
        os.mkdir(const.PATH_UPLOAD_GALLERY_TMP, 0777)
        render_gallery = True
        if id:
            try:
                photos = model.__class__.objects.get(pk=id).get_images_list()
            except:
                pass
    return {'form_class': form_class, 'photos': photos, 'render_gallery': render_gallery}


@register.inclusion_tag('dmn_gallery/dmn_gallery_detail.html')
def dmn_gallery_detail(form_id=None, img_name=None, id=None):
    widgets = {'name': HiddenInput, 'stored': HiddenInput}
    # id_details = None
    if not img_name:
        img_name = ''
    model_obj = DmnGalleryDetail
    if id:
        q = DmnGallery.objects.get(id=id)
        mod = q.details
        # id_details = q.details_id
        try:
            form = modelform_factory(model_obj, widgets=widgets, nstance=mod)
        except:
            form = modelform_factory(model_obj, widgets=widgets)
    else:
        form = modelform_factory(model_obj, widgets=widgets)
    if form_id:
        form_id = 'form_id_' + slugify(form_id)
    return {'form': form, 'form_id': form_id, 'img_name': img_name}
