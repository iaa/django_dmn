# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from dmn_utils.widgets import FileButtonWidget, ReadonlyWidget, ICheckboxSelectMultiple
from dmn import models
from django.forms.formsets import BaseFormSet
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.module_loading import import_by_path
from dmn_local import const as dmn_local_const
from django.contrib.auth.models import Group


class DmnMetaForm(ModelForm):
    class Meta:
        model = models.DmnMeta
        fields = ('meta_title', 'meta_keywords', 'meta_description')


class DmnAttachForm(ModelForm):
    class Meta:
        model = models.DmnAttach
        fields = ('attach_name', 'attach_link', 'attach_sort', 'attach_hide')
        widgets = {
            'attach_link': FileButtonWidget,
        }


class DmnAttachBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(DmnAttachBaseFormSet, self).add_fields(form, index)
        form.fields["id"] = forms.IntegerField(widget=forms.HiddenInput(), label='', required=False)


class GroupForm(ModelForm):

    class Meta:
        model = Group
        widgets = {
            'permissions': ICheckboxSelectMultiple,
        }


class DmnUserFormUpdate(UserChangeForm):

    password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'is_superuser',
                  'password',
                  'user_permissions',
                  'groups')
        widgets = {
            'password': ReadonlyWidget,
            'user_permissions': ICheckboxSelectMultiple,
            'groups': ICheckboxSelectMultiple,
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super(DmnUserFormUpdate, self).save(commit=False)
        password1 = self.cleaned_data["password1"]
        groups = self.cleaned_data.get("groups", "")
        if password1:
            user.set_password(password1)
        user.groups.clear()
        if groups:
            for g in groups:
                qg = Group.objects.get(name=g)
                user.groups.add(qg)
        if commit:
            user.save()
        return user


class DmnUserFormCreate(UserCreationForm):

    # password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    # password2 = forms.CharField(label="Подтверждение пароляasas", widget=forms.PasswordInput)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        User = get_user_model()
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'password1', 'password2')
        widgets = {
            'user_permissions': ICheckboxSelectMultiple,
            'groups': ICheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(DmnUserFormCreate, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f:
            itypes = [x.id for x in ContentType.objects.filter(Q(app_label="dj") | Q(app_label="dmn_local") | Q(app_label="shop"))]
            irez = itypes
            #plusauth = [x.id for x in ContentType.objects.filter(app_label="auth")]
            #irez = itypes + plusauth
            f.queryset = f.queryset.select_related('content_type').filter(content_type_id__in=irez)

    # def save(self, commit=True):
    #     user = super(DuserFormCreate, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user


def get_user_form(form_type):
    if form_type == 'update':
        if hasattr(dmn_local_const, 'USER_FORM_UPDATE'):
            return import_by_path(dmn_local_const.USER_FORM_UPDATE)
        else:
            return DmnUserFormUpdate
    if form_type == 'create':
        if hasattr(dmn_local_const, 'USER_FORM_CREATE'):
            return import_by_path(dmn_local_const.USER_FORM_CREATE)
        else:
            return DmnUserFormCreate
