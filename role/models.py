#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
# Create your models here.
from simple_history.models import HistoricalRecords

#job_choices = (
#    (0, _("service")),
#    (1, _("Storekeeper")),
#)
class UserProfile(models.Model):
    '''
    用户表
    '''
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.SET_NULL)
    #role = models.IntegerField(choices=job_choices, default=0)
    role = models.ForeignKey('Role',blank=True,null=True,on_delete=models.SET_NULL)
    history = HistoricalRecords()
    class Meta:
        verbose_name='用户角色关系'
    def __unicode__(self):
        return '%s-%s' % (self.user.username,self.role.name)

class Role(models.Model):
    name = models.CharField('名称',max_length=50)
    history = HistoricalRecords()
    class Meta:
        verbose_name='角色'
    def __unicode__(self):
        return '%s'%self.name

class Issuing_person(models.Model):
    '''
    出单人
    '''
    name = models.CharField('名称',max_length=50)
    history = HistoricalRecords()
    class Meta:
        verbose_name='出单人'
    def __unicode__(self):
        return '%s'%self.name
        
