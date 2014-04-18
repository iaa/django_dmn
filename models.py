# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from dmn import const
from django.utils.translation import ugettext_lazy as _
from dmn.dmn_utils import models as mixins
from picklefield.fields import PickledObjectField
# from markitup.fields import MarkupField


class DmnMenu(mixins.TreeMixin,
              mixins.BaseDmnMixin,
              mixins.IdMixin,
              mixins.HideMixin,
              mixins.NameMixin,
              mixins.CreatedUpdatedMixin1):

    link = models.CharField(max_length=765, verbose_name=_(const.MODEL_LINK))

    class Meta:
        db_table = 'dmn_menu'

    TITLE_MODEL = 'Меню админки'
    LIST_ORDER = ['id', 'name', 'link', 'hide', 'created_at', 'updated_at']
    LIST_FIELDS = {
        'hide': 'chbx',
        'created_at': 'date',
        'updated_at': 'date',
        # 'name': 'cdblcl',
        # 'name': {'color': [('all', 'green')]}
    }
    FORM_WIDGETS = {
        # 'name': 'CKeditorWidget',
        #'link': 'FileButtonWidget',
    }


class DmnDefaultMeta(models.Model):
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_keywords = models.CharField(max_length=1000, blank=True, null=True)
    meta_description = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'dmn_defaultmeta'

    class Djdmn:
        TITLE_MODEL = 'Мета по умолчанию'

        HELP = {
            'meta_title': u"""Один из наиболее важных тегов, которому поисковые системы придают огромное значение. Обязательно нужно использовать ключевые слова в теге TITLE. Кроме того, ссылка на ваш сайт в выдаче поисковой системы будет содержать текст из тега TITLE, так что это, в некотором роде, визитная карточка страницы. Именно по этой ссылке осуществляется переход посетителя поисковой системы на ваш сайт, поэтому тег TITLE должен не только содержать ключевые слова, но быть информативным и привлекательным. Как правило, в выдачу поисковой системы попадает 50-80 символов из тега TITLE, поэтому размер заголовка желательно ограничить этой длинной.""",
            'meta_keywords': u"""Список ключевых слов, через запятую, которые употреблены при написании страницы. В этот тег необходимо прописывать ключевые слова и словосочетания, которые непосредственно присутствуют на данной конкретной странице, причем в начале нужно прописывать наиболее значимые слова. Ключевые слова, которых нет в тексте поисковая машина учитывать не будет, а значимость других ключевых слов в этом теге уменьшится.""",
            'meta_description': u"""Мета-тег Description специально предназначен для задания описания страницы. Этот тег никак не влияет на ранжирование, но, тем не менее, очень важен. Многие поисковые системы (и, в частности, крупнейшая Google) отображают информацию из этого тега в результатах поиска, если этот тег присутствует на странице и его содержимое соответствует содержимому страницы и поисковому запросу. Можно с уверенностью сказать, что высокое место в результатах поиска не всегда обеспечивает большое число посетителей. Если описание ваших конкурентов в результатах выдачи будет более привлекательным, чем вашего сайта, то посетители поисковой системы выберут именно их, а не ваш ресурс. Поэтому грамотное составление мета-тега Description имеет большое значение. Описание должно быть кратким, но информативным и привлекательным, содержать ключевые слова, характерные для данной страницы.""",
        }


class DmnMeta(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_keywords = models.CharField(max_length=1000, blank=True, null=True)
    meta_description = models.TextField(max_length=1000, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'dmn_meta'

    class Djdmn:

        HELP = {
            'meta_title': u"""Один из наиболее важных тегов, которому поисковые системы придают огромное значение. Обязательно нужно использовать ключевые слова в теге TITLE. Кроме того, ссылка на ваш сайт в выдаче поисковой системы будет содержать текст из тега TITLE, так что это, в некотором роде, визитная карточка страницы. Именно по этой ссылке осуществляется переход посетителя поисковой системы на ваш сайт, поэтому тег TITLE должен не только содержать ключевые слова, но быть информативным и привлекательным. Как правило, в выдачу поисковой системы попадает 50-80 символов из тега TITLE, поэтому размер заголовка желательно ограничить этой длинной.""",
            'meta_keywords': u"""Список ключевых слов, через запятую, которые употреблены при написании страницы. В этот тег необходимо прописывать ключевые слова и словосочетания, которые непосредственно присутствуют на данной конкретной странице, причем в начале нужно прописывать наиболее значимые слова. Ключевые слова, которых нет в тексте поисковая машина учитывать не будет, а значимость других ключевых слов в этом теге уменьшится.""",
            'meta_description': u"""Мета-тег Description специально предназначен для задания описания страницы. Этот тег никак не влияет на ранжирование, но, тем не менее, очень важен. Многие поисковые системы (и, в частности, крупнейшая Google) отображают информацию из этого тега в результатах поиска, если этот тег присутствует на странице и его содержимое соответствует содержимому страницы и поисковому запросу. Можно с уверенностью сказать, что высокое место в результатах поиска не всегда обеспечивает большое число посетителей. Если описание ваших конкурентов в результатах выдачи будет более привлекательным, чем вашего сайта, то посетители поисковой системы выберут именно их, а не ваш ресурс. Поэтому грамотное составление мета-тега Description имеет большое значение. Описание должно быть кратким, но информативным и привлекательным, содержать ключевые слова, характерные для данной страницы.""",
        }


class DmnAttach(models.Model):
    HIDE_CH = ((0, 'нет'), (1, 'да'))
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    attach_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='имя документа')
    attach_link = models.CharField(max_length=500, blank=True, null=True, verbose_name='ссылка')
    attach_sort = models.PositiveIntegerField(blank=True, null=True, default=10, verbose_name='сортировка')
    attach_hide = models.PositiveIntegerField(max_length=1, choices=HIDE_CH, default=0, verbose_name='скрыто?')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'dmn_attach'

    def get_id(self):
        return self.id


# class DmnHelp(models.Model):
#     HIDE_CH = ((0, 'нет'), (1, 'да'))
#     name = models.CharField(max_length=765, verbose_name='имя')
#     text = MarkupField()
#     app = models.CharField(max_length=765, verbose_name='приложения, commasep')
#     hide = models.PositiveIntegerField(max_length=1, choices=HIDE_CH, default=0, verbose_name='скрыто?')

#     class Meta:
#         db_table = 'dmn_help'

#     class Djdmn:
#         TITLE_MODEL = 'Хелпы'
#         HELP_MODEL_GRID = None
#         HELP_MODEL_TREE = None
#         GLOBAL_HIDE = ()
#         GRID_HIDE = ['text', '_text_rendered']

#         WIDGETS = {
#             'text': 'IMarkItUpWidget',
#         }


class KV(models.Model):
    key = models.CharField(u'Key', max_length=100, unique=True)
    val = PickledObjectField(u'Value')

    class Meta(object):
        abstract = True

    @classmethod
    def get(cls, key, default=None):
        try:
            return cls.objects.get(key=key).val
        except cls.DoesNotExist:
            return default

    @classmethod
    def get_value(cls, key, default=None):
        try:
            val = cls.objects.get(key=key).val['value']
            if val and cls.get(key).get('bool', None):
                if val == '0':
                    return None
                else:
                    return val
            elif val == 'None' or val == 'none':
                return None
            elif val == '' or val == '0':
                return val
            else:
                return val
        except cls.DoesNotExist:
            return default

    @classmethod
    def put(cls, key, val):
        obj, new = cls.objects.get_or_create(key=key)
        obj.val = val
        # #tmp
        # obj.name = key
        obj.save()

    @classmethod
    def put_value(cls, key, val):
        try:
            obj = cls.objects.get(key=key)
            obj.val['value'] = val
            obj.save()
        except cls.DoesNotExist:
            print key

    @classmethod
    def rm(cls, key):
        try:
            cls.objects.get(key=key).delete()
        except cls.DoesNotExist:
            pass
