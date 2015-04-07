#coding=utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core import serializers
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from role.models import *
from order.models import Order,Product,Order_State
import datetime
import json
from models import *
from forms import *
import math

# Create your views here.
# def is_server(self):
#     if self.is_superuser:
#         return True
#     elif UserProfile.objects.get(user=self).role.name == u'客服':
#         return True
#     else:
#         return False
# 
# def is_store_manager(self):
#     if self.is_superuser:
#         return True
#     elif UserProfile.objects.get(user=self).role.name == u'仓管':
#         return True
#     else:
#         return False

# User.is_server=is_server
# User.is_store_manager=is_store_manager


@permission_required('stock.add_stock',login_url="/login")
def stock_add(request):
    if request.method=="POST":
        stock_form=StockForm(request.POST)
        if stock_form.is_valid():
            data=stock_form.cleaned_data
            name=data['name']
            detail=data['detail']
            price=data['price']
            quantity=data['quantity']
            stock_type=data['stock_type']
            stock_channel=data['stock_channel']
            stock=Stock(name=name,detail=detail,price=price,quantity=quantity,stock_type=stock_type,stock_channel=stock_channel)
            stock.save()
            return HttpResponseRedirect('/stock/info')

    else:
        stock_form=StockForm()
    form_list={
               'stock_form':stock_form,
    }
    return render(request,'stock_add.html',form_list)

@permission_required('stock.change_stock',login_url='/login')
def stock_edit(request):
    if request.method=="POST":
        #print request.POST
        name=request.POST.get('name')
        value=request.POST.get('value')
        if name=='stock_type':
            value=Stock_Type.objects.get(type_name=value)
        if name=='stock_channel':
            value=Stock_Channel.objects.get(company=value)
        info_dict={'%s'%name:value}
        stock=Stock.objects.filter(pk=request.POST.get("pk"))
        stock.update(**info_dict)
        return HttpResponse('success')

@permission_required('stock.delete_stock',login_url="/login")
def stock_remove(request):
    stock_id=request.GET.get("id")
    stock=Stock.objects.get(pk=stock_id)
    stock.delete()
    response=HttpResponse()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/stock/other';</script>")
    return response

@permission_required('stock.change_stock',login_url="/login")
def stock_other(request):
    return render(request,'stock_other.html')



@permission_required('stock.change_stock_type',login_url="/login")
def stock_type(request):
    if request.method=="POST":
        stock_type_form=Stock_TypeForm(request.POST)
        if stock_type_form.is_valid():
            data=stock_type_form.cleaned_data
            if request.GET.get("id"):
                stock_type=Stock_Type.objects.get(pk=request.GET.get("id"))
                stock_type.type_name=data['type_name']
                stock_type.save()
            else:
                name=data['type_name']
                stock_type=Stock_Type(type_name=name)
                stock_type.save()
            return HttpResponseRedirect('/stock/type')
    else:
        if request.GET.get('id'):
            stock_type_form=Stock_TypeForm(model_to_dict(Stock_Type.objects.get(pk=request.GET.get('id'))))
        else:
            stock_type_form=Stock_TypeForm()
    stock_type_data=Stock_Type.objects.all()
    form_list={
               'stock_type_data':stock_type_data,
               'stock_type_form':stock_type_form
               }
    return render(request,'stock_type.html',form_list)
@permission_required('stock.delete_stock_type',login_url="/login")
def stock_type_remove(request):
    stock_type_id=request.GET.get("id")
    stock_type=Stock_Type.objects.get(pk=stock_type_id)
    stock_type.delete()
    response=HttpResponse()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/stock/type';</script>")
    return response
@permission_required('stock.delete_stock_channel',login_url="/login")
def stock_channel(request):
    if request.method=="POST":
        stock_channel_form=Stock_ChannelForm(request.POST)
        if stock_channel_form.is_valid():
            data=stock_channel_form.cleaned_data
            if request.GET.get("id"):
                stock_channel=Stock_Channel.objects.get(pk=request.GET.get("id"))
                stock_channel.company=data['company']
                stock_channel.person=data['person']
                stock_channel.phone_number=data['phone_number']
                stock_channel.save()
            else:
                company=data["company"]
                person=data["person"]
                phone_number=data["phone_number"]
                stock_channel=Stock_Channel(company=company,person=person,phone_number=phone_number)
                stock_channel.save()
            return HttpResponseRedirect('/stock/channel')
    else:
        if request.GET.get('id'):
            stock_channel_form=Stock_ChannelForm(model_to_dict(Stock_Channel.objects.get(pk=request.GET.get('id'))))
        else:
            stock_channel_form=Stock_ChannelForm()
    stock_channel_data=Stock_Channel.objects.all()
    form_list={
               'stock_channel_data':stock_channel_data,
               'stock_channel_form':stock_channel_form
               }
    return render(request,'stock_channel.html',form_list)

@permission_required('stock.delete_stock_channel',login_url="/login")
def stock_channel_remove(request):
    stock_channel_id=request.GET.get('id')
    stock_channel=Stock_Channel.objects.get(pk=stock_channel_id)
    stock_channel.delete()
    response=HttpResponse()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/stock/channel';</script>")
    return response

@permission_required('stock.change_stock_management',login_url='/login')
def stock_management(request):
    if request.method=='POST':
        stock_mode=request.POST.get('stock_mode')
        filter_dict={}
        initial={}
        if stock_mode:
            stock_management=Stock_Management.objects.filter(stock_mode=eval(stock_mode))
            filter_dict['stock_mode']=eval(stock_mode)
        else:
            stock_management=Stock_Management.objects.all()
        product=request.POST.get('product')
        if product:
            stock_management=stock_management.filter(product=Product.objects.get(pk=int(product)))
            initial['product']=Product.objects.get(pk=int(product))
        mode=request.POST.get('mode')
        if mode:
            stock_management=stock_management.filter(mode=Stock_Mode.objects.get(pk=int(mode)))
            initial['mode']=Stock_Mode.objects.get(pk=int(mode))
        starttime=request.POST.get('starttime')
        if starttime:
            stock=Stock.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            stock=Stock.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=Stock_ManagementForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(stock_management))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            stock_management=stock_management[start_page:end_page]
            stock_mode=Stock_Mode.objects.all()
            product=Product.objects.all()
            return render(request,'stock_management_pagination.html',{'stock_management':stock_management,'stock_mode':stock_mode,
                                                                      'product':product
                                              })

        else:
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(stock_management))/5))
            stock_management=stock_management[:end_page]
            page=1
    else:
        form=Stock_ManagementForm()
        stock_management=[]
        filter_dict={}
        total_page=0
        page=0
    stock_mode=Stock_Mode.objects.all()
    product=Product.objects.all()
    info={'form':form,'stock_management':stock_management,'filter':filter_dict,
        'total_page':total_page,'current_page':page,'stock_mode':stock_mode,'product':product}
    return render(request,'stock_management.html',info)
@permission_required('stock.change_stock_management',login_url='/login')
def stock_management_edit(request):
    if request.method=="POST":
        #print request.POST
        name=request.POST.get('name')

        if name=='stock_mode':
            value=eval(request.POST.get('value[]'))

        if name=='product':
            value=Product.objects.get(name=request.POST.get('value'))
        if name=='mode':
            value=Stock_Mode.objects.get(method=request.POST.get('value'))
        info_dict={'%s'%name:value}
        stock_management=Stock_Management.objects.filter(pk=request.POST.get("pk"))
        stock_management.update(**info_dict)
        return HttpResponse('success')

@permission_required('stock.delete_stock_management',login_url='/login')
def stock_management_remove(request):
    stock_management_id=request.GET.get("id")
    stock_management=Stock_Management.objects.get(pk=stock_management_id)
    stock_management.delete()
    return HttpResponseRedirect("/stock/management")

@permission_required('stock.change_stock_mode',login_url="/login")
def stock_mode(request):
    if request.method=="POST":
        stock_mode_form=Stock_ModeForm(request.POST)
        if stock_mode_form.is_valid():
            data=stock_mode_form.cleaned_data
            if request.GET.get("id"):
                stock_mode=Stock_Mode.objects.get(pk=request.GET.get('id'))
                stock_mode.method=data['method']
                stock_mode.description=data['description']
                stock_mode.save()
            else:
                method=data['method']
                description=data['description']
                stock_mode=Stock_Mode(method=method,description=description)
                stock_mode.save()
            return HttpResponseRedirect("/stock/mode")
    else:
        if request.GET.get('id'):
            stock_mode_form=Stock_ModeForm(model_to_dict(Stock_Mode.objects.get(pk=request.GET.get('id'))))
        else:
            stock_mode_form=Stock_ModeForm()
    stock_mode_data=Stock_Mode.objects.all()
    form_list={
               'stock_mode_data':stock_mode_data,
               'stock_mode_form':stock_mode_form
               }
    return render(request,'stock_mode.html',form_list)
@permission_required('stock.delete_stock_mode',login_url='/login')
def stock_mode_remove(request):
    stock_mode_id=request.GET.get("id")
    stock_mode=Stock_Mode.objects.get(pk=stock_mode_id)
    stock_mode.delete()
    return HttpResponseRedirect("/stock/mode")

@permission_required('stock.change_stock',login_url="/permission/deny/")
def stock_order_no(request):
    if request.method=="POST":
        order_id=request.POST.get("id")
        order_no=request.POST.get("order_no")
        if order_no:
            order=Order.objects.get(pk=order_id)
            order.delivery_no=order_no
            order.state=Order_State.objects.get(name='已发货未签收')
            order.save()
            return HttpResponseRedirect("/stock/order/no")
        else:
            return HttpResponse("<script language='javascript'>alert('订单号不能为空!');window.history.go(-1);</script>")
    else:
        order_no_null=Order.objects.filter(delivery_no='').order_by('-jointime')
        order_no_success=Order.objects.exclude(delivery_no__isnull=True).exclude(delivery_no__exact='')
        form_list={
               'order_no_null':order_no_null,
               'order_no_success':order_no_success
               }
        return render(request,'stock_order_no.html',form_list)

@permission_required('stock.change_stock',login_url='/permission/deny/')
def stock_info(request):
    if request.method=='POST':
        name=request.POST.get('name')
        filter_dict={}
        initial={}
        if name:
            stock=Stock.objects.filter(name__contains=name)
            filter_dict['name']=name
        else:
            stock=Stock.objects.all()
        starttime=request.POST.get('starttime')
        if starttime:
            stock=Stock.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            stock=Stock.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=StockForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(stock))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            stock=stock[start_page:end_page]
            stock_type=Stock_Type.objects.all()
            stock_channel=Stock_Channel.objects.all()
            return render(request,'stock_pagination.html',{'stock':stock,'stock_type':stock_type,'stock_channel':stock_channel
                                              })

        else:
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(stock))/5))
            stock=stock[:end_page]
            page=1
    else:
        form=StockForm()
        stock=[]
        filter_dict={}
        total_page=0
        page=0
    stock_type=Stock_Type.objects.all()
    stock_channel=Stock_Channel.objects.all()
    info={'form':form,'stock':stock,'filter':filter_dict,
        'total_page':total_page,'current_page':page,'stock_type':stock_type,'stock_channel':stock_channel}
    return render(request,'stock_info.html',info)