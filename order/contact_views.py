#coding=utf-8

from django.contrib.auth.models import User,Group
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from models import *
from django.utils.translation import gettext as _
from django.core.cache import get_cache,cache
from role.models import *
from notifications import notify

@login_required(login_url="/login/")
def get_contact_address(request):
    response=HttpResponse()
    if request.user.is_superuser:
        contact_address=Contact_info.objects.all().values('address')
    else:
        contact_address=Contact_info.objects.filter(customer=Customer.objects.filter(
            Q(user=request.user)|Q(user__isnull=True))).values('address')
    response.write(json.dumps(list(contact_address)))
        #response.write(customer_list)
    return response

@login_required(login_url="/login/")
def get_contact_phone(request):
    response=HttpResponse()
    if request.user.is_superuser:
        contact_phone=Contact_info.objects.all().values('phone_number')
    else:
        contact_phone=Contact_info.objects.filter(customer=Customer.objects.filter(
            Q(user=request.user)|Q(user__isnull=True))).values('phone_number')
    response.write(json.dumps(list(contact_phone)))
        #response.write(customer_list)
    return response

@login_required(login_url="/login/")
def get_all_customer(request):
    response=HttpResponse()
    if request.user.is_superuser:
        customer=Customer.objects.all().values('name')
    else:
        customer=Customer.objects.filter(
            Q(user=request.user)|Q(user__isnull=True)).values('name')
    response.write(json.dumps(list(customer)))
        #response.write(customer_list)
    return response

@login_required(login_url="/login/")
def get_all_product(request):
    response=HttpResponse()
    product=Product.objects.all().values('name')
    response.write(json.dumps(list(product)))
        #response.write(customer_list)
    return response

@login_required(login_url="/login/")
def get_all_issuing_person(request):
    response=HttpResponse()
    issuing_person=Issuing_person.objects.all().values('name')
    response.write(json.dumps(list(issuing_person)))
        #response.write(customer_list)
    return response
@login_required(login_url="/login/")
def alert_message(request):
    receiver=User.objects.get(username=request.GET.get('receiver'))
    order_id=request.GET.get('order_id')
    message_info=_(u'订单号为%s,请尽快发货'%order_id)
    notify.send(request.user, recipient=receiver, verb=message_info)
    return HttpResponse("<script language='javascript'>alert('提醒成功');window.location.href=document.referrer;</script>")


@login_required(login_url="/login/")
def message_info(request):
    message=request.user.notifications.unread()
    #request.user.notifications.mark_all_as_read()
    return render(request,'message_info.html',{"alert":message})
@login_required(login_url="/login/")
def mark_all_message(request):
    request.user.notifications.mark_all_as_read()
    return HttpResponse("<script language='javascript'>alert('标记成功');window.location.href=document.referrer;</script>")