# coding=utf-8
# from django.db import models
from stock.models import *
# from role.models import Issuing_person
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.forms import ValidationError
# from django_hstore import hstore
# Create your models here.
# import datetime
# from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import HStoreField


class Product(models.Model):
    """
    产品
    """
    name = models.CharField(verbose_name='名称', max_length=100)
    price = models.DecimalField(verbose_name='价钱', max_digits=6, decimal_places=2)
    delivery_type = models.CharField(verbose_name='快递类型', max_length=100, blank=True)
    detail = models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)
    stock = models.ManyToManyField(Stock, through="Stock_Product")
    jointime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '产品'

    def __unicode__(self):

        return '%s' % self.name

    def get_stock(self):
        return "\n".join([s.name for s in self.stock.all()])

    def get_stock_info(self):
        return Stock_Product.objects.filter(product=self)


level_choices = (
    (1, _("1")),
    (2, _("2")),
    (3, _("3")),
    (4, _("4")),
    (5, _("5"))
)


class Customer_Level(models.Model):
    """
    客户水平
    """
    level = models.IntegerField(choices=level_choices, default=1)
    name = models.CharField(max_length=100)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '客户水平'

    def __unicode__(self):
        return '%s' % self.name


class Customer(models.Model):
    """
    客户信息
    """
    name = models.CharField(verbose_name='名称', max_length=100)
    sex = models.BooleanField(verbose_name='性别', default=True)
    level = models.ForeignKey(Customer_Level, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='客户等级')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='所属客服')
    # issuing_person = models.ForeignKey(Issuing_person,blank=True,null=True,on_delete=models.SET_NULL)
    data = HStoreField(blank=True, verbose_name="额外数据", null=True)
    jointime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '客户'

    def __unicode__(self):
        return '%s' % self.name

    def get_contact_info(self):
        contact = Contact_info.objects.filter(customer=self)
        if contact.filter(default=True):
            return contact.filter(default=True)
        else:
            return contact.order_by('id')

    def get_recent_order(self):
        order = Order.objects.filter(customer=self).order_by("-jointime")
        return order


class Stock_Product(models.Model):
    """
    原料产品关系
    """
    quantity = models.DecimalField(verbose_name='系数', max_digits=4, decimal_places=2)
    delivery_bill = models.BooleanField(verbose_name="是否运费", default=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    stock = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.SET_NULL)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '产品原料关系'

    def __unicode__(self):
        return '%s-%s' % (self.product.name, self.stock.name)


class Order_State(models.Model):
    """
    订单状态
    """
    name = models.CharField(verbose_name='名称', max_length=50)
    level = models.IntegerField(verbose_name="级别", blank=True, null=True)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '订单状态'

    def __unicode__(self):
        return '%s' % self.name
    

class Contact_info(models.Model):
    """
    联系方式
    """
    address = models.CharField(verbose_name='地址', max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="号码格式不正确")
    phone_number = models.CharField('手机号码', max_length=20, validators=[phone_regex], blank=True)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    default = models.BooleanField(verbose_name='默认方式', default=False)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '联系方式'

    def __unicode__(self):
        return '%s-%s' % (self.customer.name, self.phone_number)


class Order(models.Model):
    """
    订单
    """
    delivery_no = models.CharField(verbose_name='快递单号', max_length=30, default='')
    fact_money = models.DecimalField(verbose_name='实收金额', max_digits=4, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="客户")
    issuing_person = models.ForeignKey('role.Issuing_person', blank=True, null=True, on_delete=models.SET_NULL,
                                       verbose_name='出单人')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="产品")
    state = models.ForeignKey(Order_State, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="订单状态")
    remark = models.CharField(verbose_name="备注", null=True, max_length=255, blank=True)
    jointime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '订单'

    def __unicode__(self):
        return '%s' % self.delivery_no


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv', '.txt', '.xls', '.xlsx']
    if ext not in valid_extensions:
        raise ValidationError(u'Unsupported file extension')


class CustomerFile(models.Model):
    title = models.CharField(verbose_name='上传标题', max_length=100)
    file = models.FileField(upload_to='customer/%Y/%m/%d', validators=[validate_file_extension])
    jointime = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    # history = HistoricalRecords()

    class Meta:
        verbose_name = '客户导入'

    def __unicode__(self):
        return self.title


class OrderFile(models.Model):
    title = models.CharField(verbose_name='上传标题', max_length=100)
    file = models.FileField(upload_to='order/%Y/%m/%d', validators=[validate_file_extension])
    jointime = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    # history=HistoricalRecords()

    class Meta:
        verbose_name = '订单导入'

    def __unicode__(self):
        return self.title


class Order_all_info(models.Model):
    order_no = models.IntegerField(verbose_name='订单id', null=True, blank=True)
    delivery_no = models.CharField(verbose_name='快递单号', max_length=30, default='', null=True, blank=True)
    fact_money = models.CharField(verbose_name='实收金额', max_length=10, null=True, blank=True)
    customer_id = models.IntegerField(verbose_name="顾客id", null=True, blank=True)
    customer_name = models.CharField(verbose_name='客户名称', max_length=100, null=True, blank=True)
    customer_sex = models.BooleanField(verbose_name='客户性别', default=True)
    customer_level = models.IntegerField(default=1, null=True, blank=True)
    customer_level_name = models.CharField(verbose_name='客户等级名称', max_length=100, null=True, blank=True)
    user_first_name = models.CharField(verbose_name='所属客服姓名', max_length=100, null=True, blank=True)
    user_username = models.CharField(verbose_name="所属客服账号", max_length=100, null=True, blank=True)
    user_group_name = models.CharField(verbose_name="所属客服角色", max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="地址", max_length=100, null=True, blank=True)
    phone_number = models.CharField(verbose_name="手机号码", max_length=20, null=True, blank=True)
    issuing_person = models.CharField(verbose_name="出单人", max_length=100, null=True, blank=True)
    product_name = models.CharField(verbose_name="产品名称", max_length=100, null=True, blank=True)
    product_price = models.CharField(verbose_name='产品价格', max_length=10, null=True, blank=True)
    product_delivery_type = models.CharField(verbose_name="快递名称", max_length=100, null=True, blank=True)
    state_name = models.CharField(verbose_name="状态名称", max_length=100, null=True, blank=True)
    state_level = models.IntegerField(verbose_name="状态等级", null=True, blank=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)
    jointime = models.DateTimeField(verbose_name="添加时间")

    class Meta:
        verbose_name = "订单详情"

    def __unicode__(self):
        return '%s' % self.order_no


class Order_Server(models.Model):
    order = models.ForeignKey(Order, verbose_name='订单号', blank=True, null=True, on_delete=models.SET_NULL)
    content = models.CharField(verbose_name='内容', max_length=255)
    jointime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "服务纪录"

    def __unicode__(self):
        return '%s' % self.order


class Customer_Alert(models.Model):
    # customer=models.ForeignKey(Customer,verbose_name='顾客',blank=True,null=True,on_delete=models.SET_NULL)
    customer = models.CharField(verbose_name='客户', max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="号码格式不正确")
    phone_number = models.CharField('手机号码', max_length=20, validators=[phone_regex], blank=True)
    content = models.CharField(verbose_name='内容', max_length=255)
    alert_user = models.ForeignKey(User, verbose_name='提醒人', blank=True, null=True, on_delete=models.SET_NULL)
    add_user = models.CharField(verbose_name="添加人", max_length=50)
    alert_time = models.DateTimeField(verbose_name='提醒时间')
    alert_state = models.BooleanField(verbose_name='提醒状态', default=0)
    task_id = models.CharField(verbose_name='任务id', max_length='100', blank=True, null=True)
    jointime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "客户提醒"

    def __unicode__(self):
        return self.customer


class UserLog(models.Model):
    LOG_ACTIONS = (
        ('delete', _('删除')),
        ('create', _('新建')),
        ('edit', _('修改')),
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=20, choices=LOG_ACTIONS, verbose_name='操作')
    model_name = models.CharField(max_length=100, verbose_name='模型名称')
    model_object_id = models.IntegerField(verbose_name='对应的对象id')
    data = HStoreField(verbose_name='数据', null=True, blank=True)
    jointime = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        ordering = ['-jointime']
        verbose_name = '用户日记'


class Table_Design(models.Model):

    schema_model = models.CharField(max_length=50, verbose_name='表名称')
    schema_data = HStoreField(verbose_name='表结构', null=True, blank=True)
    jointime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        ordering = ['-jointime']
        verbose_name = "表逻辑"

    def __unicode__(self):
        return self.schema_model

# class Table_column(models.Model):
#     Column_Types = (
#     ('char', '字符型'),
#     ('int', '整型'),
#     ('float', '浮点型'),
#     ('text', '文本型'),
#     ('bool','布尔型'),
#     ('datetime', '日期型'),
# )
#     name=models.CharField(label='字段名',max_length=50,required=True)
#     column_type=models.ChoiceField(label="类型",choices=Column_Types,initial=Column_Types[1][0],required=False)
#     required=models.BooleanField(label='是否必填',required=False)
#     display=models.BooleanField(label='客户检索显示',required=False)