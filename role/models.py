#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
# Create your models here.


job_choices = (
    (1, _("service")),
    (2, _("Storekeeper")),
)
class UserProfile(models.Model):
    '''
    用户表
    '''
    user = models.OneToOneField(User)
    role = models.IntegerField(choices=job_choices, default=1)

class Issuing_person(models.Model):
    '''
    出单人
    '''
    name = models.CharField('名称',max_length=50)

    class Meta:
        verbose_name='出单人'
    def __unicode__(self):
        return self.name
        
