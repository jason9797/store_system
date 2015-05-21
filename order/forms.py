# -*- coding: utf-8 -*-
# from stock.models import *
# from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from role.models import *
# from django.contrib.auth.models import Group
from django import forms

class ProductForm(forms.Form):

    name = forms.CharField(label='名称', max_length=100)
    price = forms.DecimalField(label='价钱', max_digits=6, decimal_places=2)
    delivery_type = forms.CharField(label='快递类型', max_length=100)
    detail = forms.CharField(label='备注', max_length=100, required=False)
    # stock = forms.ModelMultipleChoiceField(queryset=Stock.objects.all())

level_choices = (
    (2, _("2")),
    (3, _("3")),
    (4, _("4")),
    (5, _("5"))
)


class Customer_LevelForm(forms.Form):
    """
    客户水平
    """
    level = forms.ChoiceField(choices=level_choices, initial=2)
    name = forms.CharField(max_length=20)


class CustomerForm(forms.Form):
    """
    客户信息
    """
    name = forms.CharField(max_length=100)
    sex = forms.BooleanField(initial=True, required=False,
                             widget=forms.RadioSelect(choices=[(True, _('男')), (False, _('女'))],
                                                      attrs={"class": "nav navbar-nav"}))
    level = forms.ModelChoiceField(queryset=Customer_Level.objects.all())
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False))
    usernull = forms.BooleanField(initial=False, required=False)
    # issuing_person = forms.ModelChoiceField(queryset=Issuing_person.objects.all())
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-group'}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    error_message =_("请输入正确的号码"))

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False


class Stock_ProductForm(forms.Form):
    """
    原料产品关系
    """
    quantity = forms.DecimalField(max_digits=4, decimal_places=2)
    delivery_bill = forms.BooleanField(initial=True, required=False)
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())


class Order_StateForm(forms.Form):
    """
    订单状态
    """
    name = forms.CharField(max_length=50)


class Contact_infoForm(forms.Form):
    """
    联系方式
    """
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-group'}))
    phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message=
        ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                                               ))
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())


class OrderForm(forms.Form):
    """
    订单
    """
    delivery_no = forms.CharField(max_length=30, initial='', required=False)
    fact_money = forms.DecimalField(max_digits=4,
                                    decimal_places=2,
                                    initial=0,
                                    required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    remark = forms.CharField(max_length=30, initial='', required=False)
    issuing_person = forms.ModelChoiceField(
        queryset=Issuing_person.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    state = forms.ModelChoiceField(queryset=Order_State.objects.all())

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['delivery_no'].required = False
        self.fields['fact_money'].required = False
        self.fields['remark'].required = False
        self.fields['state'].required = False


class CustomerFileForm(forms.ModelForm):

    class Meta:
        model = CustomerFile
        fields = ['title', 'file']


class OrderFileForm(forms.ModelForm):

    class Meta:
        model = OrderFile
        fields = ['title', 'file']


class User_LogForm(forms.ModelForm):

    class Meta:
        model = UserLog
        fields = ['user', 'action']


Column_Types = (
    ('char', '字符型'), ('int', '整型'), ('float', '浮点型'), ('text', '文本型'),
    ('bool', '布尔型'), ('datetime', '日期型'),)


class Table_designForm(forms.Form):
    name = forms.CharField(label='字段名', max_length=50, required=False)
    column_type = forms.ChoiceField(label="类型",
                                    choices=Column_Types,
                                    initial=Column_Types[1][0],
                                    required=False)
    required = forms.BooleanField(label='是否必填', required=False)
    # length = forms.IntegerField(widget=forms.TextInput(attrs={'size': '40','hidden':'hidden','placeholder':"字符长度",
    # 'style':'margin-left: 15px;width: 80px;'}),required=False)
    display = forms.BooleanField(label='客户检索显示', required=False)

# class table_widget(forms.Form):
#     table_int=forms.IntegerField()
#     table_char=forms.CharField(max_length=255)
#     table_float=forms.FloatField()
#     table_datetime=forms.DateTimeField()
#     table_bool=forms.BooleanField()
#     table_text=forms.Textarea()