#coding=utf-8
from django.db import models
from django import forms
# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

job_choices = (
    (1, _("service")),
    (2, _("Storekeeper")),
)
class UserForm(forms.Form):

    role = forms.ChoiceField(label='角色',choices=job_choices, initial=0)
    user = forms.ModelChoiceField(queryset=User.objects.all())


class Issuing_person(forms.Form):

    name = forms.CharField(label='出单人',max_length=50)

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField(label='旧密码',widget=forms.PasswordInput)
    new_pwd = forms.CharField(label='新密码',widget=forms.PasswordInput)
    new_pwd2= forms.CharField(label='再输一次',widget=forms.PasswordInput)
