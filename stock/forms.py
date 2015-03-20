#coding=utf-8
from models import *
from django import forms
from django.core.validators import RegexValidator
import datetime
# Create your models here.

class StockForm(forms.Form):
    '''
    原料表
    '''

    name = forms.CharField(max_length=50)
    detail = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=6, decimal_places=2)
    quantity = forms.IntegerField()
    stock_type = forms.ModelChoiceField(queryset=Stock_Type.objects.all())
    stock_channel = forms.ModelChoiceField(queryset=Stock_Channel.objects.all())
    

class Stock_TypeForm(forms.Form):

    type_name = forms.CharField(max_length=50)
class Stock_ChannelForm(forms.ModelForm):
    '''
    原料渠道
    '''
    #company = forms.CharField(max_length=100)
    #person = forms.CharField(max_length=50)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                error_message =("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    class Meta:
        model=Stock_Channel
        fields=['company','person']
class Stock_ManagementForm(forms.Form):
    '''
    库存管理
    '''
    stock_mode = forms.BooleanField(widget=forms.CheckboxInput(attrs={'value':'True'}),required=False)
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())
    mode = forms.ModelChoiceField(queryset=Stock_Mode.objects.all())


class Stock_ModeForm(forms.Form):
    '''
    出入方式
    '''
    
    method = forms.CharField(max_length=200)
    description = forms.CharField(max_length=100)
    
