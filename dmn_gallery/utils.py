# -*- coding: utf-8 -*-

import os
import shutil
import time
from hashlib import md5
from django.conf import settings
from dmn import const
from dmn_utils.spizz.pytils.translit import iaaslugify, slugify
from django.contrib.contenttypes.models import ContentType
from dmn_utils.utils import resizeimg
from dmn_gallery.models import DmnGallery, DmnGalleryDetail
from dmn_utils.utils import remove_file_from_dirs
from dmn_gallery.templatetags.dmn_gallery_widgets import dmn_gallery_detail


def upload_gallery(model, model_id, names):
    try:
        # имя папки галареи, хеш от времени
        path_name = md5(str(time.time())).hexdigest()[0:15]
        # перемещаем в нее из tmp
        path_from = const.PATH_UPLOAD_GALLERY_TMP
        path_to = os.path.join(const.PATH_UPLOAD_GALLERY, path_name)
        #filelist = [os.path.abspath(i) for i in os.listdir(path_from) if os.path.isfile(i)]
        typep = ContentType.objects.get_for_model(model)
        # массив названий картинок
        im_names = names.split(',')
        #есть ли новые картинки
        new_img = [x for x in im_names if '~' not in x]
        # перемещаем и пишем в базу
        try:
            if new_img:
                shutil.move(path_from, path_to)
            sort = 10
            for im in im_names:
                if '~' in im:
                    im_id = im.split('~')
                    id = im_id[0]
                    q = DmnGallery.objects.get(id=id)
                    q.sort = sort
                    try:
                        ifilter_q = {'name__exact': q.img, 'stored': False}
                        c = DmnGalleryDetail.objects.get(**ifilter_q)
                        q.details_id = c.id
                        c.stored = True
                        c.save()
                    except:
                        pass
                    q.save()
                else:
                    q = DmnGallery(content_type_id=typep.id, object_id=model_id, img=im, path=path_name, sort=sort, hide=0)
                    q.save()
                sort += 10
            return True
        except:
            return False
    except:
        return False


def aj_delete_hide_img(name, id=None, path=None, confirm=False, more=False):
    rez = False
    if confirm == 'yes':
        # если галерея
        if id and path:
            if path != 'hide' and path != 'recovery':
                try:
                    # удаляем из базы
                    DmnGallery.objects.filter(id=id).delete()
                    rez = True
                except:
                    rez = False
        # если tmp файлы
        else:
            rez = remove_file_from_dirs(const.UPLOAD_TMP, name)
        if path == 'hide':
            try:
                DmnGallery.objects.filter(id=id).update(hide=1)
                rez = True
            except:
                rez = False
        if path == 'recovery':
            try:
                DmnGallery.objects.filter(id=id).update(hide=0)
                rez = True
            except:
                rez = False
    return rez
