#coding=utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core import serializers
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from role.models import *
import datetime
import json
from models import *
from forms import *

# Create your views here.
def is_server(self):
    if self.is_superuser:
        return True
    elif UserProfile.objects.get(user=self).role.name == u'客服':
        return True
    else:
        return False

def is_store_manager(self):
    if self.is_superuser:
        return True
    elif UserProfile.objects.get(user=self).role.name == u'仓管':
        return True
    else:
        return False

User.is_server=is_server
User.is_store_manager=is_store_manager

def store_required(login_url=None):
    return user_passes_test(lambda u:u.is_store_manager(),login_url=login_url)

@store_required(login_url="/login")
def stock_home(request):
    if request.method=="POST":
        form=StockForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            name=data['name']
            detail=data['detail']
            price=data['price']
            quantity=data['quantity']
            stock_type=data['stock_type']
            stock_channel=data['stock_channel']
            stock=Stock(name=name,detail=detail,price=price,quantity=quantity,stock_type=stock_type,stock_channel=stock_channel)
            stock.save()
            return HttpResponseRedirect('/stock/home')
    stock_data=Stock.objects.all()
    stock_form=StockForm()
    stock_type=Stock_TypeForm()
    stock_mode=Stock_ModeForm()
    stock_management=Stock_ManagementForm()
    stock_channel=Stock_ChannelForm()
    form_list={
               'stock_data':stock_data,
               'stock_form':stock_form,
               'stock_type':stock_type,
               'stock_mode':stock_mode,
               'stock_management':stock_management,
               'stock_channel':stock_channel
    }
    return render(request,'stock_home.html',form_list)
@store_required(login_url="/login")
def stock_type_add(request):
    if request.method=="POST":
        form=Stock_TypeForm(request.POST)
        if form.is_valid():
            name=request.POST.get('type_name')
            stock_type=Stock_Type(type_name=name)
            stock_type.save()
            return HttpResponseRedirect('/stock/home')
        else:
            pass
@store_required(login_url="/login")
def stock_type_remove(request):
    stock_type_id=request.GET.get("id")
    stock_type=Stock_Type.objects.get(pk=stock_type_id)
    stock_type.delete()
    response=HttpResponse()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/stock/home';</script>")
    return response
@store_required(login_url="/login")
def stock_channel_add(request):
    if request.method=="POST":
        form=Stock_ChannelForm(request.POST)
        if form.is_valid():
            company=request.POST.get("company")
            person=request.POST.get("person")
            phone_number=request.POST.get("phone_number")
            stock_channel=Stock_Channel(company=company,person=person,phone_number=phone_number)
            stock_channel.save()
            return HttpResponseRedirect('/stock/home')
        else:
            pass

@store_required(login_url="/login")
def stock_channel_remove(request):
    stock_channel_id=request.GET.get('id')
    stock_channel=Stock_Channel.objects.get(pk=stock_channel_id)
    stock_channel.delete()
    response=HttpResponse()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/stock/home';</script>")
    return response

#@store_required(login_url="/login")
#def stock_management(request):

