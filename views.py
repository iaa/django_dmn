# -*- coding: utf-8 -*-

# import os
# import markdown
# from django.utils.encoding import force_unicode
# from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import View, ListView, DeleteView, CreateView, UpdateView
from dmn_utils import views as utils_views
from dmn_utils import models as utils_models
from dmn import const
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from dmn.mixins import AjaxableResponseMixin, RedirectMixin, HasPermMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request
from django.forms.models import modelform_factory
from django.contrib import messages
from django.contrib.auth import get_user_model
from dmn.forms import get_user_form, GroupForm
from django.contrib.auth.models import Group, Permission
from dmn_local.views import *
# from django.forms.formsets import formset_factory


@ajax_request
@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def index(request):
    return render(request, 'dmn/index.html')


class SecureView(View):
    @method_decorator(user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL))
    def dispatch(self, *args, **kwargs):
        return super(SecureView, self).dispatch(*args, **kwargs)


class List(SecureView, ListView):
    context_object_name = "list"
    template_name = "dmn/list.html"
    paginate_by = int(const.DEFAULT_GRID_PERPAGE)
    title_model = None
    list_action_hide = []
    hide_fields = []
    model_name = None
    list_fields = []
    id_hide = []
    exclude = {}
    str_represent = 'name'

    def dispatch(self, request, *args, **kwargs):
        self.sort = request.GET.get('sort', 'asc')
        self.sort_by = request.GET.get('sort_by', None)
        if self.sort:
            if self.sort == 'asc':
                self.sort = 'desc'
            else:
                self.sort = "asc"
        if request.GET.get('per_page', None):
            self.paginate_by = request.GET['per_page']
        self.search_by_field = request.GET.get('search_by_field', None)
        self.search_word = request.GET.get('search_word', None)
        if kwargs.get('model', None):
            self.model_name = kwargs['model']
        if not self.model:
            self.model = utils_models.getModelByName(self.model_name)
        if 'hide_field' in request.GET:
            self.hide_fields = request.GET.getlist('hide_field', [])
        self.title_model = getattr(self.model, 'TITLE_MODEL', self.title_model)
        self.list_action_hide = getattr(self.model, 'LIST_ACTION_HIDE', self.list_action_hide)
        self.list_fields = getattr(self.model, 'LIST_FIELDS', self.list_fields)
        self.id_hide = getattr(self.model, 'ID_HIDE', self.id_hide)
        self.str_represent = getattr(self.model, 'STR_REPRESENT', self.str_represent)
        if hasattr(self.model, 'get_columns'):
            self.get_columns = self.model.get_columns(self.hide_fields)
        else:
            self.get_columns = utils_models.base_get_columns(self.model, self.hide_fields)
        self.related_table = request.GET.get('related_table', None)
        self.related_key = request.GET.get('related_key', None)
        self.related_value = request.GET.get('related_value', None)
        self.user_group = request.GET.get('user_group', None)
        self.user_is_active = request.GET.get('user_is_active', None)
        self.user_is_staff = request.GET.get('user_is_staff', None)
        return super(List, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        sort_by = 'id'
        if self.id_hide:
            self.exclude = {'id__in': self.id_hide}
        if self.sort_by:
            sort_by = self.sort_by
            if self.sort == 'desc':
                sort_by = '-' + self.sort_by
        if self.search_by_field and self.search_word:
            try:
                search = {'%s__%s' % (self.search_by_field, 'contains'): self.search_word}
                qs = self.model.objects.order_by(sort_by).filter(**search).exclude(**self.exclude)
            except:
                search = {'%s__%s__%s' % (self.search_by_field, self.str_represent, 'contains'): self.search_word}
                qs = self.model.objects.order_by(sort_by).filter(**search).exclude(**self.exclude)
        # If query by reladed base
        elif self.related_table and self.related_key and self.related_value:
            search = {'%s__%s' % (self.related_table, self.related_key): self.related_value}
            qs = self.model.objects.order_by(sort_by).filter(**search).exclude(**self.exclude)
        # Is users by groups (active)
        elif self.user_group and self.user_is_active and self.user_is_active == '1':
            search = {'groups__name': self.user_group, 'is_active': 1}
            qs = self.model.objects.order_by(sort_by).filter(**search).exclude(**self.exclude)
        # If users by groups (unactive)
        elif self.user_group and self.user_is_active and self.user_is_active == '0':
            search = {'groups__name': self.user_group, 'is_active': 0}
            qs = self.model.objects.order_by(sort_by).filter(**search).exclude(**self.exclude)
        else:
            qs = self.model.objects.order_by(sort_by).exclude(**self.exclude)
        return qs

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        context['model'] = self.model_name
        context['mess_list_find_field'] = _(const.BUTT_LIST_FIND_FIELD)
        context['mess_list_find_field_2'] = _(const.MESS_LIST_FIND_FIELD)
        context['mess_add'] = _(const.BUTT_ADD)
        context['mess_list_mark_delete'] = _(const.BUTT_LIST_MARK_DELETE)
        context['mess_list_find_field'] = _(const.BUTT_LIST_FIND_FIELD)
        context['mess_head'] = _(const.BUTT_LIST_FIND_FIELD)
        context['mess_cont'] = _(const.MESS_LIST_FIND_FIELD)
        context['title_model'] = self.title_model
        context['action_hide'] = self.list_action_hide
        context['model_columns'] = self.get_columns
        context['list_fields'] = self.list_fields
        context['sort'] = self.sort
        context['sort_by'] = self.sort_by
        context['paginate_by'] = self.paginate_by
        context['hidden_fields'] = self.hide_fields
        return context


class Tree(SecureView, ListView):
    template_name = 'dmn/tree.html'
    context_object_name = "nodes"
    related_table = None
    related_list = None
    related_link_list = 'list'
    exclude = {}
    title_model = ''
    help_model = ''

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('model', None):
            self.model_name = kwargs['model']
        if not self.model:
            self.model = utils_models.getModelByName(self.model_name)
        self.title_model = getattr(self.model, 'TITLE_MODEL', self.title_model)
        self.help_model = getattr(self.model, 'HELP_MODEL_TREE', self.help_model)
        return super(Tree, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.exclude(**self.exclude).order_by('tree_id', 'lft')

    def get_context_data(self, **kwargs):
        context = super(Tree, self).get_context_data(**kwargs)
        context['model'] = self.model_name
        context['title_model'] = self.title_model
        context['help_model'] = self.help_model
        context['related_table'] = self.related_table
        context['related_list'] = self.related_list
        context['related_link_list'] = self.related_link_list
        return context


class CreateUpdateMixin(AjaxableResponseMixin,
                        RedirectMixin,
                        HasPermMixin,
                        SecureView,):
    template_name = 'dmn/createup_cbv.html'
    success_url = '/dmn/'
    pk_url_kwarg = 'id'
    fly_success = 'Undefined'
    title_model = ''
    help_model_createup = ''
    permission = []

    def dispatch(self, request, *args, **kwargs):
        self.gallery = []
        self.request = request
        self.success_url = self.redirect()
        self.pk = kwargs.get('id', None)
        self.model_name = kwargs.get('model', None)
        if self.pk:
            self.permission = ['change']
        else:
            self.permission = ['add']
        if self.model_name:
            self.model = utils_models.getModelByName(self.model_name)
        if 'gallery' in request.POST:
            self.gallery = request.POST['gallery']
        self.title_model = getattr(self.model, 'TITLE_MODEL', self.title_model)
        self.help_model_createup = getattr(self.model, 'HELP_MODEL_CREATEUP', self.help_model_createup)
        # Если parent пришел из дерева, добавим в форму
        if 'parent' in request.GET:
            self.initial.update(parent=request.GET['parent'])
        elif self.initial.get('parent', None):
            del self.initial['parent']
        return super(CreateUpdateMixin, self).dispatch(request, *args, **kwargs)

    def get_form_widgets(self):
        widdict = {}
        if hasattr(self.model, 'FORM_WIDGETS'):
            if self.model.FORM_WIDGETS:
                for k, v in self.model.FORM_WIDGETS.items():
                    try:
                        widget = v
                    except:
                        widget = ''
                    widdict.update({k: widget})
                return widdict

    def get_form_class(self, **kwargs):
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model
            return modelform_factory(model, fields=self.fields, widgets=self.get_form_widgets(), **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateUpdateMixin, self).get_context_data(**kwargs)
        context['title_model'] = self.title_model
        context['model_name'] = self.model_name
        context['model'] = self.model
        context['help_model_createup'] = self.help_model_createup
        context['id'] = self.pk
        return context


class DeleteMixin(DeleteView,
                  RedirectMixin,
                  HasPermMixin,
                  SecureView):
    fly_success = const.FLY_DELETED_SUCCESS
    permission = ['delete']

    def dispatch(self, request, *args, **kwargs):
        self.gallery = []
        self.success_url = self.redirect()
        self.request = request
        self.pk_url_kwarg = 'id'
        self.model_name = kwargs.get('model', None)
        if (not self.model) and (self.model_name is not None):
            self.model = utils_models.getModelByName(self.model_name)
        if request.GET.get('destroy_arr', None):
            self.queryset = self.model.objects.filter(id__in=request.GET['destroy_arr'].split(','))
        if 'gallery' in request.POST:
            self.gallery = request.POST['gallery']
        # self.object = self.get_object()
        # Если parent пришел из дерева, добавим в форму
        if 'parent' in request.GET:
            self.initial.update(parent=request.GET['parent'])
        return super(DeleteMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get('destroy_arr', None):
            pk = request.GET['destroy_arr']
        else:
            pk = self.kwargs.get(self.pk_url_kwarg, None)
        mess = '%s %s' % (unicode(self.fly_success), pk)
        messages.success(self.request, mess)
        return self.delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.queryset is not None:
            return self.queryset
        else:
            return super(DeleteMixin, self).get_object(queryset=None)


class Create(CreateUpdateMixin, CreateView):
    fly_success = _(const.FLY_CREATED_SUCCESS)
    pass


class Update(CreateUpdateMixin, UpdateView):
    fly_success = _(const.FLY_UPDATED_SUCCESS)
    pass


class UserCreate(CreateUpdateMixin, CreateView):
    fly_success = _(const.FLY_CREATED_SUCCESS)
    form_class = get_user_form('create')
    model = get_user_model()


class UserUpdate(CreateUpdateMixin, UpdateView):
    fly_success = _(const.FLY_UPDATED_SUCCESS)
    model = get_user_model()
    form_class = get_user_form('update')


class GroupList(List):
    title_model = 'Группы'
    model_name = 'group'
    model = Group


class GroupCreate(CreateUpdateMixin, CreateView):
    fly_success = _(const.FLY_CREATED_SUCCESS)
    model = Group
    form_class = GroupForm


class GroupUpdate(CreateUpdateMixin, UpdateView):
    fly_success = _(const.FLY_UPDATED_SUCCESS)
    model = Group
    form_class = GroupForm


class GroupDestroy(DeleteMixin):
    model = Group


class PermisionList(List):
    title_model = 'Права'
    model_name = 'permission'
    model = Permission


class PermisionCreate(CreateUpdateMixin, CreateView):
    fly_success = _(const.FLY_CREATED_SUCCESS)
    model = Permission


class PermisionUpdate(CreateUpdateMixin, UpdateView):
    fly_success = _(const.FLY_UPDATED_SUCCESS)
    model = Permission


class PermisionDestroy(DeleteMixin):
    model = Permission


class Destroy(DeleteMixin):
    pass


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def toggle(request, model, attr, id, *args, **kwargs):
    try:
        model_obj = utils_models.getModelByName(model)
        permission = ['change']
        if not utils_views.has_perm(request, model_obj, permission):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dmn'))
        m = model_obj.objects.get(pk=id)
        sattr = getattr(m, attr)
        gattr = True if sattr == 0 else False
        kw = {attr: gattr}
        if attr == 'hide' and hasattr(m, 'get_descendants'):
            t = m.get_ancestors()
            if t:
                for x in t:
                    if x.hide == 1:
                        mess = u'%s (поз. %s)' % (_(settings.FLY_ERR_UPDATED_PARENT), str(m.id))
                        messages.error(request, mess)
                        return model
        m.__setattr__(attr, gattr)
        m.save()
        mess = u'%s (поз. %s)' % (_(const.FLY_UPDATED_SUCCESS), str(m.id))
        messages.success(request, mess)
        # Если mptt и если скрываем/восст., то скрываем/восст. потомков
        if attr == 'hide' and hasattr(m, 'get_descendants'):
            m.get_descendants().update(**kw)
    except:
        messages.warning(request, _(const.FLY_ERROR_GLOBAL))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dmn'))


@csrf_exempt
@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def fastedit(request, model, *args, **kwargs):
    actviews.w_fastedit(request, model, *args, **kwargs)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', None))


#----------------------------------------------------------------------
#-------------------- TREE --------------------------------------------
#----------------------------------------------------------------------

class CatTree(Tree):
    template_name = 'dmn/cat_tree.html'
    exclude = {'hide': True}
    # related_table = 'Dmnmenu'
    # related_list = 'Dmnmenu'


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def tree_change_pid(request, model, id, pid, position):
    # Объект модели
    obj = utils_models.getModelByName(model)
    # permission = ['change']
    if not utils_views.has_perm(request, obj, ['change']):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dmn'))
    # Экземпляр объекта модели
    this_ob = obj.objects.get(id=id)
    # Предок
    parent_ob = obj.objects.get(id=pid)
    if position == 'inside':
        obj.tree.move_node(this_ob, parent_ob, position='first-child')
    else:
        try:
            # id предка объекта
            par_from = [x.id for x in this_ob.get_ancestors() if this_ob.get_ancestors()]
            # id предка объекта назначения
            par_to = [x.id for x in parent_ob.get_ancestors() if parent_ob.get_ancestors()]
            par = par_from[0]
            par_par = par_to[0]
        except:
            par = None
            par_par = None
        if not par == par_par:
            par_ob = obj.objects.get(id=par_par)
            obj.tree.move_node(this_ob, par_ob, position='last-child')
        if position == 'before':
            this_ob.move_to(parent_ob, position='left')
        if position == 'after':
            this_ob.move_to(parent_ob, position='right')
    mess = u"%s (поз. %d)" % (_(const.FLY_UPDATED_SUCCESS), int(id))
    messages.success(request, mess)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', None))


@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def aj_sort_grid(request):
    try:
        model_obj = i_get_model(request.GET['model'])
        ids = [int(x) for x in request.GET['ids'].split(',')]
        sort = [int(x) for x in request.GET['sort'].split(',')]
        sort.sort()
        rez = zip(ids, sort)
        for id, sort in rez:
            q = model_obj.objects.get(pk=id)
            q.sort = sort
            q.save()
        messages.success(request, 'Ок, отсортировано')
    except:
        messages.error(request, 'Err, сортировка не удалась')
    return HttpResponse('ok')


#----------------------------------------------------------------------
#-------------------- YANDEX MAIL -------------------------------------
#----------------------------------------------------------------------

@user_passes_test(utils_views.user_login, login_url=const.LOGIN_URL)
def yamail(request):
    return render(request, 'yamail/login.html')
