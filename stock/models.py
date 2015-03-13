#coding=utf-8
from django.db import models
from django.core.validators import RegexValidator
import datetime
# Create your models here.

class Stock(models.Model):
    '''
    原料表
    '''

    name = models.CharField(verbose_name='名称',max_length=50)
    detail = models.CharField(verbose_name='名称',max_length=100)
    price = models.DecimalField(verbose_name='单价',max_digits=6, decimal_places=2)
    quantity = models.IntegerField(verbose_name='数量')
    stock_type = models.ForeignKey('Stock_Type',verbose_name='类别')
    stock_channel = models.ForeignKey('Stock_Channel',verbose_name='进货渠道')
    jointime = models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    class Meta:
        verbose_name='原料'

    def __unicode__(self):
        return self.name


class Stock_Type(models.Model):
    '''
    原料类别
    '''
    type_name = models.CharField(verbose_name='类别名称',max_length=50)

    class Meta:
        verbose_name='原料类别'

    def __unicode__(self):
        return self.type_name
class Stock_Channel(models.Model):
    '''
    原料渠道
    '''
    company = models.CharField(verbose_name='公司名称',max_length=100)
    person = models.CharField(verbose_name='联系人',max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(verbose_name='手机号码',max_length=20,validators=[phone_regex], blank=True)
    jointime=models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    class Meta:
        verbose_name='原料渠道'

    def __unicode__(self):
        return self.company

class Stock_Management(models.Model):
    '''
    库存管理
    '''
    stock_mode = models.BooleanField(verbose_name='出/入库',default=True)
    stock = models.ForeignKey(Stock,verbose_name='原料')
    mode = models.ForeignKey('Stock_Mode',verbose_name='出入方式')
    jointime =models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    class Meta:
        verbose_name='库存管理'

    def __unicode__(self):
        return self.stock_mode

class Stock_Mode(models.Model):
    '''
    出入方式
    '''
    
    method = models.CharField(verbose_name='方式',max_length=200)
    description = models.CharField(verbose_name='描述',max_length=100)

    class Meta:
        verbose_name='出入方式'
    def __unicode__(self):
        return self.method
