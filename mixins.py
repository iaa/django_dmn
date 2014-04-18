# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from dmn_gallery.utils import upload_gallery
from dmn_utils import views as utils_views
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict
import json
from django.http import HttpResponse, HttpResponseRedirect


class RedirectMixin(object):
    def redirect(self):
        redirect_mix = self.request.session.get('redirect_mix', None)
        redirect_ref = self.request.META.get('HTTP_REFERER', None)
        if not redirect_mix and redirect_ref and self.request.build_absolute_uri() != redirect_ref:
            self.request.session['redirect_mix'] = redirect_ref
        elif redirect_mix and redirect_ref and self.request.build_absolute_uri() != redirect_ref:
            self.request.session['redirect_mix'] = redirect_ref
        elif not redirect_mix and not redirect_ref:
            self.request.session['redirect_mix'] = '/dmn'
        return self.request.session['redirect_mix']


class HasPermMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if self.permission:
            if not utils_views.has_perm(request, self.model, self.permission):
                return HttpResponseRedirect(self.success_url)
        return super(HasPermMixin, self).dispatch(request, *args, **kwargs)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form, non_field_msg='General form errors'):
        if self.request.is_ajax():
            verbose_errors = ErrorDict()
            field_errors = []
            for field, errors in form.errors.items():
                if field == NON_FIELD_ERRORS:
                    key = non_field_msg
                else:
                    key = unicode(form.fields[field].label)
                verbose_errors[key] = errors
                field_errors.append(field)
            out = {'field_errors': field_errors, 'errors': verbose_errors}
            return self.render_to_json_response(out, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            inst = form.save()
            if self.gallery:
                upload_gallery(self.model, inst.id, self.gallery)
            response = HttpResponse(status=200)
            mess = '%s %s' % (unicode(self.fly_success), inst.id)
            messages.success(self.request, mess)
            response['Location'] = self.success_url
            return response
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)
