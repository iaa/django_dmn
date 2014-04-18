# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.loading import get_model
from django.contrib.auth import get_user_model
from dmn import const
from django.utils.encoding import python_2_unicode_compatible


def getModelByName(modelName):
    """
    return the Model class with the given model class name
    """
    try:
        if modelName == 'User' or modelName == 'user':
            User = get_user_model()
            return User
        for x in settings.INSTALLED_APPS:
            try:
                model_obj = get_model(x, modelName)
                if model_obj:
                    return model_obj
            except:
                pass
    except:
        pass


def base_get_columns(cls, hidden=[], dmn_list=True):
        """
        Return the list of dicts of self columns with verbose names.
        Be sure if cls.LIST_ORDER that contains all colums, just sorted.
        """
        out = []
        list_hide = []
        # print cls._meta.get_field('test').name
        if hasattr(cls, 'LIST_HIDE'):
            list_hide = cls.LIST_HIDE
        if hasattr(cls, 'LIST_ORDER') and cls.LIST_ORDER:
            ilist = cls.LIST_ORDER
        else:
            ilist = (x.name for x in cls._meta.fields)
        for i in ilist:
            if i not in list_hide and i not in hidden:
                out.append({'name': cls._meta.get_field(i).name, 'verbose': cls._meta.get_field(i).verbose_name})
        return out


class ModelOptionsMixin(object):
    TITLE_MODEL = const.MODEL_TITLE_DEFAULT
    HELP_MODEL_LIST = None
    HELP_MODEL_TREE = None
    HELP_MODEL_CREATEUP = None
    STR_REPRESENT = 'name'
    GLOBAL_HIDE = ()
    LIST_ACTION_HIDE = []  # LIST_ACTION_HIDE = ['create', 'update', 'destroy']
    LIST_HIDE = ['parent_id']
    LIST_ORDER = []
    LIST_FIELDS = {}
    FOR_IAA = {'name': 'admin'}
    FORM_WIDGETS = {}
    ID_HIDE = []


class BaseDmnMixin(ModelOptionsMixin,
                   models.Model):

    def __init__(self, *args, **kwargs):
        super(BaseDmnMixin, self).__init__(*args, **kwargs)
        # print self

    class Meta:
        abstract = True

    @classmethod
    def get_verbose_name(cls, field=None):
        if field is not None:
            return cls._meta.get_field(field).verbose_name

    @classmethod
    def get_columns(cls, hidden=[], dmn_list=True):
        return base_get_columns(cls, hidden=hidden, dmn_list=True)


class IdMixin(models.Model):

    id = models.AutoField(primary_key=True, verbose_name=const.MODEL_ID)

    class Meta:
        abstract = True


class HideMixin(models.Model):

    hide = models.BooleanField(verbose_name=const.MODEL_HIDDEN)

    class Meta:
        abstract = True


class ActiveMixin(models.Model):

    is_active = models.BooleanField(verbose_name=const.MODEL_ACTIVE)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class NameMixin(models.Model):

    name = models.CharField(max_length=765, verbose_name=const.MODEL_NAME)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TitleMixin(models.Model):

    title = models.CharField(max_length=765, verbose_name=const.MODEL_TITLE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class SortMixin(models.Model):

    sort = models.PositiveIntegerField(default=20, verbose_name=const.MODEL_SORT)

    class Meta:
        abstract = True


class CreatedUpdatedMixin1(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=const.MODEL_CREATED_AT)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=const.MODEL_UPDATED_AT)

    class Meta:
        abstract = True


class TreeMixin(MPTTModel):
    """
    Tree mixin must be first
    """
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=const.MODEL_PARENT)

    class MPTTMeta:
        order_insertion_by = ['hide']

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class RegistrationMixin1(models.Model):

    first_name = models.CharField(max_length=100, verbose_name=const.MODEL_FIRSTNAME)
    last_name = models.CharField(max_length=100, verbose_name=const.MODEL_LASTNAME)
    surname = models.CharField(max_length=100, verbose_name=const.MODEL_SURNAME, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100, verbose_name=const.MODEL_PHONE, null=True, blank=True)

    class Meta:
        abstract = True

