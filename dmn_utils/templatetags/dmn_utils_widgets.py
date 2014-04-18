# -*- coding: utf-8 -*-

from django import template
from dmn_utils import utils

register = template.Library()


@register.simple_tag
def resizeimg(img_name=None, path1=None, path2=None, size=None, crop=True):
    if size:
        size = [int(n) for n in size.split(',')]
    rez = utils.resizeimg(img_name, path1, path2, size, crop)
    return rez
