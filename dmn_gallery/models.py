# -*- coding: utf-8 -*-

import os
from django.db.models.signals import pre_delete, post_save
from dmn.dmn_utils.utils import remove_file_from_dirs, clear_empty_dir
from dmn.dmn_gallery import settings
from dmn.dmn_gallery import settings as gallery_settings
from django.db import models
from dmn.dmn_utils import models as mixins
# from gallery_local.models import Mixins
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import receiver
from django.core.cache import cache


class DmnGalleryDetail(mixins.BaseDmnMixin,
                       mixins.IdMixin,
                       mixins.HideMixin,
                       mixins.NameMixin):
    stored = models.BooleanField(default=False)
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'титл')
    description = models.TextField(blank=True, null=True, verbose_name=u'описание')

    class Meta:
        db_table = 'dmn_gallery_detail'


class DmnGallery(mixins.BaseDmnMixin,
                 mixins.IdMixin,
                 mixins.HideMixin,
                 mixins.NameMixin,
                 mixins.SortMixin,
                 mixins.CreatedUpdatedMixin1):
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    img = models.CharField(max_length=150)
    path = models.CharField(max_length=30)
    details = models.OneToOneField(DmnGalleryDetail, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'dmn_gallery'

    def save(self, *args, **kwargs):
        try:
            ifilter = {'name__exact': self.img, 'stored': False}
            q = DmnGalleryDetail.objects.get(**ifilter)
            self.details_id = q.id
            q.stored = True
            q.save()
        except:
            pass
        super(DmnGallery, self).save(*args, **kwargs)

    class Djdmn:
        # FORM_CREATE = DuserFormCreate
        # FORM_UPDATE = DuserFormUpdate
        GRID_HIDE = ['first_name', 'last_name', 'password']
        FIELDS = {
            'is_staff':
                # Чекбокс
                {'chbx': ''},
            'is_active':
                # Чекбокс
                {'chbx': ''},
            'is_superuser':
                # Чекбокс
                {'chbx': ''},
        }

        HELP = {
                'group': u'Только для дополнительных приложений',
               }


class DmnGalleryMixin(models.Model):
    photos = generic.GenericRelation(DmnGallery)

    class Meta(object):
        abstract = True

    class Djdmn:
        HELP_MODEL_CREATEUP = """Для загрузки изображений счелкните вкладку "картинки",
        если у вас современный браузер, то вы можете загружать множество картинок одновременно.
        Первая картинка в галерее считается главной. Для сортировки картинок просто перетаскивайте
        их мышкой, для действий с картинкой - пользуйтесь правой кнопкой миши. (Скрытые картинки на сайте не
        отображаются, но подлежат восстановлению, удаленные картинки уничтожаются безвозвратно)"""

    def gtest(self):
        pass
        # print self.name

    def get_images(self):
        try:
            return self.photos.order_by('sort')
        except:
            return None

    def get_images_list(self, details=False, hide=True, nofirst=False):
        try:
            if hide:
                q = self.get_images()
            else:
                q = self.get_nohide_images()
            iurl = gallery_settings.UPLOAD_GALLERY_URL
            if nofirst:
                if details:
                    return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide, 'details': x.details} for x in q if x != self.get_first_image()]
                return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide} for x in q if x != self.get_first_image()]
            if details:
                return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide, 'details': x.details} for x in q]
            return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide} for x in q]
        except:
            return None

    def get_images_list_nohide(self, details=False, hide=False, nofirst=False):
        try:
            if hide:
                q = self.get_images()
            else:
                q = self.get_nohide_images()
            iurl = gallery_settings.UPLOAD_GALLERY_URL
            if nofirst:
                if details:
                    return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide, 'details': x.details} for x in q if x != self.get_first_image()]
                return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide} for x in q if x != self.get_first_image()]
            if details:
                return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide, 'details': x.details} for x in q]
            return [{'path': os.path.join(iurl, x.path), 'img': x.img, 'id': x.id, 'hide': x.hide} for x in q]
        except:
            return None

    def get_nohide_images(self):
        try:
            return self.photos.order_by('sort').filter(hide=False)
        except:
            return None

    def get_count_images(self):
        try:
            return self.photos.order_by('sort').filter(hide=0).count()
        except:
            return None

    def get_first_image(self):
        try:
            key = 'get_first_image_%s' % str(self.id)
            cached = cache.get(key)
            if cached is not None:
                return cached
            res = self.get_nohide_images()[0]
            cache.set(key, res)
            return res
        except:
            return None


def pre_delete_dmn_gallery(sender, **kwargs):
    obj = kwargs['instance']
    try:
        key = 'get_first_image_%s' % str(obj.object_id)
        cache.delete(key)
    except:
        pass
    try:
        # рекурсивно удаляем файл изо всех подпапок галереи
        rez = remove_file_from_dirs(os.path.join(settings.UPLOAD_GALLERY, obj.path), obj.img)
        # рекурсивное удаление опустевших папок
        if rez:
            clear_empty_dir(os.path.join(settings.UPLOAD_GALLERY, obj.path))
            # удаляем связь
            DmnGalleryDetail.objects.get(pk=obj.details_id).delete()

    except:
        pass


@receiver(post_save, sender=DmnGallery)
def on_change(instance, **kwargs):
    key = 'get_first_image_%s' % str(instance.object_id)
    cache.delete(key)

pre_delete.connect(pre_delete_dmn_gallery, sender=DmnGallery)
# post_save.connect(postSaveGallery, sender=Gallery)
