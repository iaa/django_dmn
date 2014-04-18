# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from dmn import const


def user_login(user):
    return user.is_authenticated() and user.is_staff


def has_perm(request, model, permission):
    typ = ContentType.objects.get_for_model(model)
    typ_app_label = typ.app_label
    typ_model = typ.model
    perm = ['%s.%s_%s' % (typ_app_label, p, typ_model) for p in permission]
    if not request.user.has_perms(perm):
        mess = unicode(const.FLY_PERM_WARNING)
        messages.warning(request, mess)
        return False
    return True
