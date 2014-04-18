# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from dmn import models
from dmn import const
from django.utils.translation import ugettext_lazy as _
from dmn_utils import models as utils_models
import markdown
from django.utils.safestring import mark_safe
from django.utils import formats

register = template.Library()


@register.inclusion_tag('dmn_widgets/iDmenu.html')
def dmenu(user):
    ifilter = {}
    iexclude = {}
    #iexclude['hide'] = '1'
    ifilter['hide'] = False
    nodes = models.DmnMenu.objects.filter(**ifilter).exclude(**iexclude).order_by('tree_id', 'lft')
    if not user.username == 'iaa':
        if hasattr(models.DmnMenu.Djdmn, 'FOR_IAA'):
            fields_all = models.DmnMenu._meta.fields
            # есть ли тут поля для superuser
            for_superuser = [x.name for x in fields_all if x.name in models.DmnMenu.Djdmn.FOR_IAA]
            for x in nodes:
                for z in for_superuser:
                    if x.name.encode('utf-8') == models.DmnMenu.Djdmn.FOR_IAA.get(z, None):
                        iexclude[z] = x.name
    nodes = models.DmnMenu.objects.filter(**ifilter).exclude(**iexclude).order_by('tree_id', 'lft')
    try:
        if user.first_name:
            username = user.first_name
        else:
            username = user.username
    except:
        username = 'Noname'
    return {'nodes': nodes, 'username': username}


@register.simple_tag
def dmn_list(model_name, field, list_fields, data, id=None):
    obj = utils_models.getModelByName(model_name)
    id = data.id
    if hasattr(data, field):
        value = getattr(data, field)
    else:
        value = None
    out = value
    if field in list_fields:
        try:
            if not isinstance(list_fields[field], dict):
            # Это чекбокс?
                if list_fields[field] == 'chbx':
                    if value == 1:
                        out = '<input class="chbx_toggle" checked="checked" id="%s" model="%s" type="checkbox" value="%s" name="%s">' % (id, model_name, value, field)
                    else:
                        out = '<input class="chbx_toggle" id="%s" model="%s" type="checkbox" value="%s" name="%s">' % (id, model_name, value, field)
                if list_fields[field] == 'chbx_closed':
                    if value == 1:
                        out = '<input class="chbx_toggle" checked="checked" id="%s" model="%s" type="checkbox" value="%s" name="%s" disabled="disabled">' % (id, model_name, value, field)
                    else:
                        out = '<input class="chbx_toggle" id="%s" model="%s" type="checkbox" value="%s" name="%s">' % (id, model_name, value, field)
                # Это дата?
                if list_fields[field] == 'date':
                    out = formats.date_format(value, format='SHORT_DATETIME_FORMAT')
                if 'dblcl' in list_fields[field]:
                    out = '<div class="child_dblcl badge" style="background:none; border:solid 1px gray; color:black; font-size: 11px; font-weight: normal" id="%s" model="%s" name="%s" editor="false">%s</div>' % (id, model_name, field, value)
                if 'cdblcl' in list_fields[field]:
                    out = '<div class="child_dblcl badge" style="background:none; border:solid 1px gray; color:black; font-size: 11px; font-weight: normal" id="%s" model="%s" name="%s" editor="true">%s</div>' % (id, model_name, field, value)
                # Это ссылка?
                if list_fields[field] == 'link' or obj.LIST_FIELDS[field] == 'link_self':
                    value = str(value).replace('http://', '')
                    value = str(value).replace('www', '')
                    value = str(value).replace(' ', '')
                    if list_fields[field] == 'link':
                        out = '<a href="http://%s" target="_blank">http://%s</a>' % (value, value)
                    if list_fields[field] == 'link_self':
                        out = '<a href="http://%s">http://%s</a>' % (value, value)
                if list_fields[field] == 'dblcl':
                    out = '<div class="child_dblcl badge" style="background:none; border:solid 1px gray; color:black; font-size: 11px; font-weight: normal" id="%s" model="%s" name="%s" editor="false">%s</div>' % (id, model_name, field, value)
                if list_fields[field] == 'cdblcl':
                    out = '<div class="child_dblcl badge" style="background:none; border:solid 1px gray; color:black; font-size: 11px; font-weight: normal" id="%s" model="%s" name="%s" editor="true">%s</div>' % (id, model_name, field, value)
            else:
                # Это цвет для исключения?
                if 'outcolor' in list_fields[field] and (str(value)) != str(list_fields[field]['outcolor'][0]):
                    out = '<span class="badge" style="background-color:%s">%s</span>' % (list_fields[field]['outcolor'][1], value)
                # Это цвет для большего значения?
                if 'maxcolor' in list_fields[field] and int(value) > int(list_fields[field]['maxcolor'][0]):
                    out = '<span class="badge" style="background-color:%s">%s</span>' % (list_fields[field]['maxcolor'][1], value)
                # Это цвет для меньшего значения?
                if 'mincolor' in list_fields[field] and int(value) < int(list_fields[field]['mincolor'][0]):
                    out = '<span class="badge" style="background-color:%s">%s</span>' % (list_fields[field]['mincolor'][1], value)
                # Это цвет для совпадения?
                if 'color' in list_fields[field]:
                    for x in list_fields[field]['color']:
                        # если один цвет для всех значений
                        if str(x[0]) == 'all':
                            out = '<span class="badge" style="background-color:%s">%s</span>' % (x[1], value)
                        if str(value) == str(x[0]):
                            out = '<span class="badge" style="background-color:%s">%s</span>' % (x[1], value)
            # # Это картинка?
            # if 'img' in model_obj.Djdmn.FIELDS[field]:
            #     out = '<img class="thumb" src="%s">' % dmnutils.resizeimg(value, isize=[60, 60], crop=False)
            # # Это картинка из галереи?
            # if 'gal_img' in model_obj.Djdmn.FIELDS[field]:
            #     try:
            #         im_obj = model_obj.objects.get(pk=id)
            #         first_im = im_obj.get_first_image()
            #         count_im = im_obj.get_count_images()
            #         im = first_im.img
            #         ipath = first_im.path
            #         out = '<a href="/media/dmn_gallery/gallery/%s/%s" target="blank"><img class="thumb" src="%s"> (%s шт.)</a>' % (ipath, im, dmnutils.resizeimg(im, isize=[60, 60], path1='/media/dmn_gallery/gallery/'+ipath, crop=False), count_im)
            #     except:
            #         out = 'Error!'
            # # Это ссыль?
            # if 'url' in model_obj.Djdmn.FIELDS[field]:
            #     url = b'%s%s/' % (model_obj.Djdmn.FIELDS[field]['url']['page'], value)
            #     out = b'<a class="colorbox_iframe label label-info" href="%s">%s</a>' % (url, model_obj.Djdmn.FIELDS[field]['url']['name'])
        except:
            pass
    return out


@register.simple_tag
def dmeta(meta=None):
    def_meta = models.Defaultmeta.objects.get(id=1)
    out = ''
    if meta:
        try:
            if meta.meta_title:
                title = meta.meta_title
            else:
                title = def_meta.meta_title
            if meta.meta_keywords:
                keywords = meta.meta_keywords
            else:
                keywords = def_meta.meta_keywords
            if meta.meta_description:
                description = meta.meta_description
            else:
                description = def_meta.meta_description
        except:
            pass
    else:
        title = def_meta.meta_title
        keywords = def_meta.meta_keywords
        description = def_meta.meta_description
    out += """<meta name="keywords" content="%s" /><meta name="description" content="%s" /><meta name="generator" content="" /><title>%s</title>""" % (keywords, description, title)
    return out


@register.simple_tag
def dattach(attach=None):
    out = ''
    if attach:
        out += """<div class=well style="margin-left: 50px;"><h3>Документы:</h3>"""
        for x in attach:
            try:
                if x.attach_name:
                    out += b"""<a href="%s" target="_blank">%s</a><br>""" % (x.attach_link, x.attach_name)
                else:
                    print x.attach_link
                    out += b"""<a href="%s" target="_blank">%s</a><br>""" % (x.attach_link, x.attach_link)
            except:
                return ''
        out += """</div>"""
    return out


@register.simple_tag
def wgridactions(model, id=None):
    out = '<a'
    # Получаем объект модели по имени, колонки и назв. таблицы
    model_obj = utils.i_get_model(model)
    if hasattr(model_obj, 'Djdmn'):
        if hasattr(model_obj.Djdmn, 'ACTIONS'):
            for x in model_obj.Djdmn.ACTIONS:
                if x['iclass']:
                    iclass = x['iclass']
                else:
                    iclass = ''
                if x['link']:
                    ilink = x['link']
                else:
                    ilink = ''
                if x['title']:
                    ititle = x['title']
                else:
                    ititle = ''
                if id:
                    iid = id
                else:
                    iid = ''
                out += """ class="btn btn-small ibtn-action" href="%s" id="%s"><i class="%s"></i> %s""" % (ilink, iid, iclass, ititle)
    out += '</a>'
    return out


@register.filter
def imarkdown(txt):
    return mark_safe(markdown.markdown(txt))


@register.filter
def mess(value):
    if hasattr(const, value):
        return _(getattr(const, value))


@register.inclusion_tag('dmn_widgets/pagination.html')
def pagination(pdata, pp, model, path):
    prev = []
    next = []
    ipagination = {}
    if pdata.number - 3 in pp.page_range:
        prev.append(pdata.number - 3)
    if pdata.number - 2 in pp.page_range:
        prev.append(pdata.number - 2)
    if pdata.number - 1 in pp.page_range:
        prev.append(pdata.number - 1)
    if pdata.number + 1 in pp.page_range:
        next.append(pdata.number + 1)
    if pdata.number + 2 in pp.page_range:
        next.append(pdata.number + 2)
    if pdata.number + 3 in pp.page_range:
        next.append(pdata.number + 3)
    if 1 in prev:
        prev.remove(1)
    if pp.num_pages in next:
        next.remove(pp.num_pages)
    ipagination['last_page'] = pp.num_pages
    ipagination['next'] = next
    ipagination['prev'] = prev
    if pdata.has_next:
        ipagination['i_next'] = pdata.next_page_number
    if pdata.has_previous:
        ipagination['i_previous'] = pdata.previous_page_number
    ipagination['current'] = pdata.number
    return {'ipagination': ipagination, 'model': model, 'path': path}
