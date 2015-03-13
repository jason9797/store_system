#-*- coding: utf-8 -*-
from django import forms
from forms import *
from models import *
from stock.models import *
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

class ProductForm(forms.Form):

    name = forms.CharField(label='名称',max_length=100)
    price = forms.DecimalField(label='价钱',max_digits=6, decimal_places=2)
    delivery_type = forms.CharField(label='快递类型',max_length=100,initial=True)
    #stock = forms.ModelMultipleChoiceField(queryset=Stock.objects.all())


level_choices = (
    (1, _("vip")),
    (2, _("vvip")),
    (3, _("vvvip")),
)
class Customer_LevelForm(forms.Form):
    '''
    客户水平
    '''
    level = forms.ChoiceField(choices=level_choices, initial=1)


class CustomerForm(forms.Form):
    '''
    客户信息
    '''
    name = forms.CharField(max_length=100)
    sex = forms.BooleanField(initial=True)
    level = forms.ModelChoiceField(queryset=Customer_Level.objects.all())

class Stock_ProductForm(forms.Form):
    '''
    原料产品关系
    '''
    quantity = forms.DecimalField(max_digits=4, decimal_places=2)
    delivery_bill = forms.BooleanField(initial=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())


class Order_StateForm(forms.Form):
    '''
    订单状态
    '''
    name = forms.CharField(max_length=50)


class Contact_infoForm(forms.Form):
    '''
    联系方式
    '''
    address = forms.CharField(max_length=30)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                error_message =("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())


class OrderForm(forms.Form):
    '''
    订单
    '''
    delivery_no = forms.CharField(max_length=30,initial='',required=False)
    fact_money = forms.DecimalField(max_digits=4, decimal_places=2,initial=0,required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    issuing_person = forms.ModelChoiceField(queryset=Issuing_person.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    state = forms.ModelChoiceField(queryset=Order_State.objects.all())

