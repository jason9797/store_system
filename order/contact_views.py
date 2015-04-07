#coding=utf-8
__author__ = 'jason_lee'
from django.contrib.auth.models import User,Group
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from models import *
@login_required(login_url="/login/")
def get_contact_address(request):
    response=HttpResponse()
    if request.user.is_superuser:
        contact_address=Contact_info.objects.all().values('address')
    else:
        contact_address=Contact_info.objects.filter(customer=Customer.objects.filter(
            Q(user=User.objects.get(pk=23))|Q(user__isnull=True))).values('address')
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
            Q(user=User.objects.get(pk=23))|Q(user__isnull=True))).values('phone_number')
    response.write(json.dumps(list(contact_phone)))
        #response.write(customer_list)
    return response