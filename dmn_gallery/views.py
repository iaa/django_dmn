# -*- coding: utf-8 -*-
import os
import shutil
import time
from hashlib import md5
from django.http import HttpResponse
from django.template import RequestContext, loader
from dmn_gallery.utils import aj_delete_hide_img as aj_del_hide_img
from django.views.decorators.csrf import csrf_exempt
# from dmn_gallery.forms import DetailsForm
from dmn_gallery.models import DmnGalleryDetail
# from dmn_utils.forms import Dform
from dmn import const
from django.conf import settings
from dmn_utils.utils import resizeimg
from dmn_gallery.templatetags.dmn_gallery_widgets import dmn_gallery_detail
from dmn_utils.spizz.pytils.translit import iaaslugify, slugify
from django.forms.models import modelform_factory
from django.forms.widgets import HiddenInput
from django_ajax.decorators import ajax


@ajax
def upload_gallery(request):
    path_to = const.PATH_UPLOAD_GALLERY_TMP
    out = ''
    if not os.path.exists(path_to):
        os.mkdir(path_to, 0777)
    if request.is_ajax():
        if request.FILES:
            for f in request.FILES.lists()[0][1]:
                fname = md5(str(time.time())).hexdigest()[0:5] + iaaslugify(f.name)
                dest = os.path.join(path_to, fname)
                with open(dest, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                result = resizeimg(os.path.join(settings.MEDIA_URL, 'dmn_gallery', 'tmp', fname))
                tpl = loader.get_template('dmn_gallery/upload_gallery.html')
                cont = RequestContext(request,
                                      dict(r_name=fname,
                                      r_slug_name=slugify(fname),
                                      r_upload_tmp=os.path.join(settings.MEDIA_URL, 'dmn_gallery', 'tmp', fname),
                                      r_result=result))
                out += tpl.render(cont)
    print dmn_gallery_detail()
    return HttpResponse(out)


@csrf_exempt
def upload_gallery_details(request):
    widgets = {'name': HiddenInput}
    data = request.POST.copy()
    data['name'] = data['img_name']
    if 'id' in data:
        q = DmnGalleryDetail.objects.get(pk=data['id'])
        f = modelform_factory(DmnGalleryDetail, widgets=widgets, instance=q)(data)
    else:
        f = modelform_factory(DmnGalleryDetail, widgets=widgets)(data)
    f.save()
    return HttpResponse('ok')


def aj_delete_hide_img(request):
    if 'del_img_id' in request.GET and 'del_img_path' in request.GET:
        rez = aj_del_hide_img(request.GET['del_img_name'], request.GET['del_img_id'], request.GET['del_img_path'], request.GET['confirm'])
    else:
        rez = aj_del_hide_img(request.GET['del_img_name'])
    if rez:
        return HttpResponse('ok')
    else:
        return HttpResponse('error')
