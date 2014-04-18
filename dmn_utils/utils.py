# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.core.mail import mail_admins
from PIL import Image, ImageOps


def send_mail_admin_error(request, error_text, *args, **kwargs):
    subject = request.META['HTTP_HOST']
    if mail_admins(subject, error_text, *args, **kwargs):
        return True
    return False


def resizeimg(img=None, path1=None, path2=None, isize=None, crop=True, no_photo=None):
    try:
        root_r = settings.MEDIA_ROOT
        root_u = settings.MEDIA_URL
        tmb = [128, 128]
        no_photo = 'no-image.png'
        if img == 'None' or not img:
            # root_p = gallery_settings.DMN_GALLERY
            # root_u = gallery_settings.DMN_GALLERY_URL
            imgs = os.path.join(root_u, 'dmn_gallery', 'no_image', no_photo)
        elif path1:
            imgs = os.path.join(path1, img)
            # Если это галерея
            if path2:
                imgs = os.path.join(path1, path2, img)
        else:
            imgs = str(img)
        find1 = imgs.replace(root_u, '')
        find = os.path.split(find1)
        path_root = os.path.join(root_r, find[0])
        path_from = os.path.join(path_root, find[1])
        im = Image.open(path_from)
        if not isize:
            isize = tmb
        if isize[1] == 0:
            wpercent = (float(isize[0]) / float(im.size[0]))
            isize[1] = int((float(im.size[1]) * float(wpercent)))
        if isize[0] == 0:
            wpercent = (float(isize[1]) / float(im.size[1]))
            isize[0] = int((float(im.size[0]) * float(wpercent)))
        tmb_path = str(isize[0]) + 'x' + str(isize[1])
        path_to = os.path.join(path_root, tmb_path)
        if not os.path.exists(path_to):
            os.mkdir(path_to, 0777)
        if not os.path.isfile(os.path.join(path_to, find[1])):
            if not crop:
                im.thumbnail(isize, Image.ANTIALIAS)
            else:
                im = ImageOps.fit(im, isize, Image.ANTIALIAS)
            im.save(path_to + '/' + find[1], quality=100)
        url = os.path.join('/', root_u, find[0])
        return os.path.join(url, tmb_path, find[1])
    except:
        return ''


# Recursively removing empty directories
def clear_empty_dir(path):
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in dirs:
                fname = os.path.join(root, name)
                if not os.listdir(fname):
                    os.removedirs(fname)
        return True
    except:
        return False


# Recursively removing file from directories
def remove_file_from_dirs(path, myfile):
    try:
        for root, dirs, files in os.walk(path):
            for one_file in files:
                if one_file == myfile:
                    os.remove(os.path.join(root, one_file))
        return True
    except:
        return False


# Get files from dir
def get_files_from_dir(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
