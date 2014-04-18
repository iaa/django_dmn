# -*- coding: utf-8 -*-
from django import forms
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from dmn_utils.utils import resizeimg
from markitup.widgets import MarkItUpWidget
# from django.conf import settings


class CKeditorWidget(forms.Textarea):

    attrs = {}

    def __init__(self, config=None):
        self.conf = config
        if not self.conf:
            self.conf = {}

    class Media:

        js = ('/static/dmn/ckeditor2/ckeditor.js',)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        value = force_unicode(value)  # important when pre-fill content contains unicode
        rendered = super(CKeditorWidget, self).render(name, value, attrs)
        return mark_safe(self.media) + rendered + mark_safe(
                                    u"""<script type="text/javascript">
                                    $(function(){
                                        CKEDITOR.replace('%s', %s);
                                    });
                                    </script>
                                    """ % (name, self.conf))


class FileButtonWidget(forms.TextInput):

    attrs = {}

    def render(self, name, value=None, attrs=None):
        text = ''
        value = force_unicode(value)
        if value != 'None' and value != '' and value:
            try:
                img = resizeimg(value, crop=False)
                text += u"""<img src="%s">""" % img
            except:
                pass
        text += u"""<input readonly type="text" name="%(name)s" value="%(value)s" id="id_%(name)s">""" % vars()
        text += u"""<a name="id_%(name)s" class="btn primary repl" href="#" onclick="repl_func(this.name)">Выбрать файл</a>""" % vars()
        text += u"""<a class="btn primary" href="#" onclick="repl_func_clear('id_%(name)s')">Очистить</a>""" % vars()
        return mark_safe(text)


class ReadonlyWidget(forms.TextInput):

    attrs = {}

    def render(self, name, value=None, attrs=None):
        value = force_unicode(value)
        text = u"""<input readonly type="text" name="%(name)s" value="%(value)s" id="id_%(name)s">""" % vars()
        return mark_safe(text)


class ReadonlyIntWidget(forms.TextInput):

    attrs = {}

    def render(self, name, value=0, attrs=None):
        if not value:
            value = 0
        value = force_unicode(value)
        text = u"""<input readonly type="text" name="%(name)s" value="%(value)s" id="id_%(name)s">""" % vars()
        return mark_safe(text)


class ICheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, *args, **kwargs):
        output = super(ICheckboxSelectMultiple, self).render(*args, **kwargs)
        return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'').replace(u'</li>', u'').replace(u'label', u'label class="checkbox"'))


class OptionsCheckboxSelectMultiple(ICheckboxSelectMultiple):

    def render(self, *args, **kwargs):
        output = super(OptionsCheckboxSelectMultiple, self).render(*args, **kwargs)
        return (
            mark_safe(self.media) +
            mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'').replace(u'</li>', u'').replace(u'label', u'label class="checkbox ch_options"').replace(u'input', u'input class="ch_options textareaClosed"'))
        )


class IRadioSelect(forms.RadioSelect):

    def render(self, *args, **kwargs):
        output = super(IRadioSelect, self).render(*args, **kwargs)
        return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'').replace(u'</li>', u'').replace(u'label', u'label class="checkbox"'))


class DateWidget(forms.TextInput):

    attrs = {}

    class Media:
        css = {
            '': ('/static/dmn/fort/plugins/datepicker/css/datepicker.css',)
        }
        js = ('/static/dmn/fort/plugins/datepicker/js/bootstrap-datepicker.js',)

    def render(self, name, value=None, attrs=None):
        value = force_unicode(value)
        text = u"""<input type="text" name="%(name)s" value="%(value)s" id="id_%(name)s" data-date-format="yyyy-mm-dd">""" % vars()
        text += u"""
            <script>$(function(){
                $('#id_%(name)s').datepicker();
            })</script>

        """ % vars()
        return mark_safe(self.media) + mark_safe(text)


class ColorWidget(forms.TextInput):

    attrs = {}

    class Media:
        css = {
            '': ('/static/dmn/colorpicker/css/colorpicker.css',)
        }
        js = ('/static/dmn/colorpicker/js/colorpicker.js',)

    def render(self, name, value=None, attrs=None):
        value = force_unicode(value)
        text = u"""<input type="text" name="%(name)s" value="%(value)s" id="colorpickerField">""" % vars()
        text += u"""
            <script>
                $('#colorpickerField').ColorPicker({
                    onSubmit: function(hsb, hex, rgb, el) {
                        $(el).val(hex);
                        $(el).ColorPickerHide();
                    },
                    onBeforeShow: function () {
                        $(this).ColorPickerSetColor(this.value);
                    }
                })
                .bind('keyup', function(){
                    $(this).ColorPickerSetColor(this.value);
                });
            </script>

        """ % vars()
        return mark_safe(self.media) + mark_safe(text)

class IMarkItUpWidget(MarkItUpWidget):
    pass
