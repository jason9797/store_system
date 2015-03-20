#coding=utf-8
from django.db import models
from stock.models import Stock
from role.models import Issuing_person
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
# Create your models here.
import datetime
from simple_history.models import HistoricalRecords
class Product(models.Model):
    '''
    产品
    '''
    name = models.CharField(verbose_name='名称',max_length=100)
    price = models.DecimalField(verbose_name='价钱',max_digits=6, decimal_places=2)
    delivery_type = models.CharField(verbose_name='快递类型',max_length=100,blank=True)
    stock = models.ManyToManyField(Stock,through="Stock_Product")
    jointime =models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name='产品'
    def __unicode__(self):
        return '%s'%self.name
    def get_stock(self):
        return "\n".join([s.name for s in self.stock.all()])

level_choices = (
    (1, _("vip")),
    (2, _("vvip")),
    (3, _("vvvip")),
)
class Customer_Level(models.Model):
    '''
    客户水平
    '''
    level = models.IntegerField(choices=level_choices, default=1)
    history = HistoricalRecords()
    class Meta:
        verbose_name='客户水平'
    def __unicode__(self):
        return '%s'%self.level
    
class Customer(models.Model):
    '''
    客户信息
    '''
    name = models.CharField(verbose_name='名称',max_length=100)
    sex = models.BooleanField(verbose_name='性别',default=True)
    level = models.ForeignKey(Customer_Level)
    user = models.ForeignKey(User)
    issuing_person = models.ForeignKey(Issuing_person,null=True)
    jointime =models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name='客户'
    def __unicode__(self):
        return '%s'%self.name

class Stock_Product(models.Model):
    '''
    原料产品关系
    '''
    quantity = models.DecimalField(verbose_name='系数',max_digits=4, decimal_places=2)
    delivery_bill = models.BooleanField(verbose_name="是否运费",default=True)
    product = models.ForeignKey(Product)
    stock = models.ForeignKey(Stock)
    history = HistoricalRecords()
    class Meta:
        verbose_name='产品原料关系'
    def __unicode__(self):
        return '%s-%s'%(self.product.name,self.stock.name)

class Order_State(models.Model):
    '''
    订单状态
    '''
    name = models.CharField(verbose_name='名称',max_length=50)
    history = HistoricalRecords()
    class Meta:
        verbose_name='订单状态'
    def __unicode__(self):
        return '%s'%self.name
    

class Contact_info(models.Model):
    '''
    联系方式
    '''
    address = models.CharField(verbose_name='地址',max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField('手机号码',max_length=20,validators=[phone_regex], blank=True)
    customer = models.ForeignKey(Customer)
    history = HistoricalRecords()
    class Meta:
        verbose_name='联系方式'
    def __unicode__(self):
        return '%s-%s'%(self.customer.name,self.phone_number)
    
class Order(models.Model):
    '''
    订单
    '''
    delivery_no = models.CharField(verbose_name='快递单号',max_length=30,default='')
    fact_money = models.DecimalField(verbose_name='实收金额',max_digits=4, decimal_places=2,default=0)
    customer = models.ForeignKey(Customer)
    issuing_person = models.ForeignKey(Issuing_person,null=True)
    product = models.ForeignKey(Product)
    state = models.ForeignKey(Order_State)
    jointime =models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name='订单'
    def __unicode__(self):
        return '%s'%self.delivery_no
    
    
    
