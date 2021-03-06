# coding=utf-8
# from django.db import models
# from django import forms
# Create your models here.
from django.contrib.auth.models import Permission, ContentType
from django.utils.translation import gettext as _
from django.contrib.admin.widgets import FilteredSelectMultiple
# from django.db.models import Q
from django.contrib.auth.models import User, Group
from models import *
from django import forms
job_choices = (
    (1, _("service")),
    (2, _("Storekeeper")),
)

# class UserForm(forms.Form):
#
#     role = forms.ChoiceField(label='角色',choices=job_choices, initial=0)
#     user = forms.ModelChoiceField(queryset=User.objects.all())


class UserForm(forms.ModelForm):
    # permissions=forms.ModelMultipleChoiceField(label=_('权限'),queryset=Permission.objects.filter(
    #     content_type__in=ContentType.objects.filter(id__range=[7,18])),
    #     widget=FilteredSelectMultiple("verbose name",is_stacked=False))
    username = forms.CharField(label=_('用户名'), max_length=20)
    group = forms.ModelChoiceField(label=_('角色'), queryset=Group.objects.all())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'email', 'group')
# class UserpermissionForm(forms.ModelForm):
#     user_permissions=forms.ModelMultipleChoiceField(label=_('权限'),queryset=Permission.objects.filter(
#         content_type__in=ContentType.objects.filter(id__range=[7,18])),
#         widget=FilteredSelectMultiple("verbose name",is_stacked=False))
#     class Meta:
#         model=User
#         fields=('user_permissions',)


class UsergroupForm(forms.ModelForm):
    groups = forms.ModelChoiceField(label=_('组'), queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('groups',)

    def __init__(self, *args, **kwargs):
        super(UsergroupForm, self).__init__(*args, **kwargs)
        self.fields['groups'].required = False
        # self.groups=forms.ModelChoiceField(label=_('组'),queryset=Group.objects.all(),
        # widget=forms.RadioSelect(),required=False)


class GroupForm(forms.ModelForm):
    # permission_choices=[u'原料',u'产品',u'客户水平',u'客户',u'订单状态',u'联系方式',u'订单',u'出单人',u'角色',u'客户导入',u'订单导入']
    # permissions=forms.ModelMultipleChoiceField(label=_('权限'),queryset=Permission.objects.filter(
    # content_type__in=ContentType.objects.filter(name__in=permission_choices)),
    # widget=FilteredSelectMultiple("verbose name",is_stacked=False))
    permission_choices = ['stock', 'product', 'customer_level', 'customer',
                          'contact_info', 'order', 'issuing_person', 'role',
                          'customerfile', 'orderfile']
    permissions = forms.ModelMultipleChoiceField(label=_('权限'), queryset=Permission.objects.filter(
        content_type__in=ContentType.objects.filter(
            model__in=permission_choices)), widget=FilteredSelectMultiple("verbose name", is_stacked=False))

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        # fields='__all__'
        # labels={
        #     'name':_('角色'),
        #     'permissions':_('权限'),
        # }
        # help_texts={
        #     'name':_('输入角色名称'),
        #     'permission':_('选择角色权限')
        # }
        # error_messages={
        #     'name':{
        #         'max_length':_('名称长度太长')
        #     }
        # }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].required = False


class Issuing_personForm(forms.Form):

    name = forms.CharField(label='出单人', max_length=50)


class RoleForm(forms.Form):

    name = forms.CharField(label='角色', max_length=50)


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)


class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField(label='旧密码', widget=forms.PasswordInput)
    new_pwd = forms.CharField(label='新密码', widget=forms.PasswordInput)
    new_pwd2 = forms.CharField(label='再输一次', widget=forms.PasswordInput)


class Server_goalForm(forms.Form):
    user = forms.ModelChoiceField(label=_('客服'), queryset=User.objects.filter(is_superuser=False))
    goal_quantity = forms.IntegerField(label=_('目标出单量'), required=False, initial=0)
    goal_money = forms.DecimalField(label=_('目标销售额'), max_digits=7, decimal_places=2, initial=0)
    default = forms.BooleanField(initial=False, required=False,
                                 widget=forms.RadioSelect(choices=[(True, _('目标销售量')), (False, _('目标出单量'))], attrs={"class": "nav navbar-nav"}))


class Server_cutForm(forms.Form):
    server = forms.ModelChoiceField(label=_('客服'), queryset=User.objects.filter(is_superuser=False))
    cut_percentage = forms.DecimalField(label=_("提成系数"), max_digits=2, decimal_places=2, required=False)


class Issuing_person_cutForm(forms.Form):
    issuing_person = forms.ModelChoiceField(label=_('出单人'), queryset=Issuing_person.objects.all())
    cut_percentage = forms.DecimalField(label=_("提成系数"), max_digits=2, decimal_places=2, required=False)