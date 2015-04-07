#coding=utf-8
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from role.models import *
from django.shortcuts import render
from models import *
from django.db.models import Count,Sum
import datetime
from collections import OrderedDict
from datetime import timedelta
from role.views import admin_required
@admin_required(login_url='/login')
def income_reporter(request):
    if request.method=="POST":
        # if request.POST.get("last_month"):
        #     starttime=datetime.date.today().replace(day=1)-timedelta(days=1).replace(day=1).strftime('%Y-%m-%d')
        #     endtime=(datetime.date.today().replace(day=1)-timedelta(days=1)).strftime('%Y-%m-%d')
        # elif request.POST.get("this_month"):
        #     starttime=datetime.date.today().replace(day=1).strftime('%Y-%m-%d')
        #     endtime=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')
        # else:
        starttime=request.POST.get('starttime')
        endtime=request.POST.get('endtime')

        order_data=Order.objects.filter(jointime__gte=starttime).filter(jointime__lte=endtime).extra({'day':'date(jointime)'}).values('day','product').order_by('day')
        day_money=OrderedDict()
        #print order_data
        for i in order_data:
            if i['day'] not in day_money:
                day_money[i['day']]=Product.objects.get(pk=i['product']).price
            else:
                day_money[i['day']]+=Product.objects.get(pk=i['product']).price
        #return render(request,'reporter_chart.html',{'data':day_money})
    else:
        day_money=[]
        starttime=''
        endtime=''
    this_month_starttime=datetime.date.today().replace(day=1)
    this_month_endtime=datetime.date.today()-timedelta(days=1)
    this_format_starttime=this_month_starttime.strftime('%Y-%m-%d')
    this_format_endtime=this_month_endtime.strftime('%Y-%m-%d')
    last_month_starttime=(datetime.date.today().replace(day=1)-timedelta(days=1)).replace(day=1)
    last_month_endtime=datetime.date.today().replace(day=1)-timedelta(days=1)
    last_format_starttime=last_month_starttime.strftime('%Y-%m-%d')
    last_format_endtime=last_month_endtime.strftime('%Y-%m-%d')
    this_order_data=Order.objects.filter(jointime__gte=this_format_starttime).filter(jointime__lte=this_format_endtime).extra({'day':'date(jointime)'}).values('day','product')

    this_day_money=OrderedDict()
    for i in range(1,this_month_endtime.day+1):
            #this_day_money[this_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
        this_day_money[str(i)]=0
        #print this_day_money
    for i in this_order_data:
        this_day_money[str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
    last_order_data=Order.objects.filter(jointime__gte=last_format_starttime).filter(jointime__lte=last_format_endtime).extra({'day':'date(jointime)'}).values('day','product')
    last_day_money=OrderedDict()
    for i in range(1,last_month_endtime.day+1):
            #last_day_money[last_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
        last_day_money[str(i)]=0
    for i in last_order_data:
        last_day_money[str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
        #print last_day_money
    return render(request,'income_reporter.html',{'this_month_data':this_day_money,'last_month_data':last_day_money,'data':day_money,
                                                  'starttime':starttime,'endtime':endtime})

@admin_required(login_url='/login')
def issuing_person_reporter(request):
    if request.method=="POST":
        starttime=request.POST.get('starttime')
        endtime=request.POST.get('endtime')
        issuing_person=request.POST.get('issuing_person')
        order_data=Order.objects.filter(jointime__gte=starttime).filter(jointime__lte=endtime).filter(issuing_person=Issuing_person.objects.get(name=issuing_person)).extra({'day':'date(jointime)'}).values('day','product').order_by('day')
        day_money=OrderedDict()
        #print order_data
        for i in order_data:
            if i['day'] not in day_money:
                day_money[i['day']]=Product.objects.get(pk=i['product']).price
            else:
                day_money[i['day']]+=Product.objects.get(pk=i['product']).price

    else:
        starttime=''
        endtime=''
        day_money=[]
    this_month_starttime=datetime.date.today().replace(day=1)
    this_month_endtime=datetime.date.today()-timedelta(days=1)
    this_format_starttime=this_month_starttime.strftime('%Y-%m-%d')
    this_format_endtime=this_month_endtime.strftime('%Y-%m-%d')
    this_order_data=Order.objects.filter(jointime__gte=this_format_starttime).filter(jointime__lte=this_format_endtime).extra({'day':'date(jointime)'}).values('day','product','issuing_person')
    #this_day_money=OrderedDict()
#    for i in range(1,this_month_endtime.day+1):
            #this_day_money[this_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
#        this_day_money[str(i)]=0
    all_person={}
    issuing_person=Issuing_person.objects.all()
    day_dict={}
    for i in range(1,this_month_endtime.day+1):
        day_dict[str(i)]=0
    for i in this_order_data:
        if Issuing_person.objects.get(pk=i['issuing_person']) in all_person:
            pass
        else:
            #day_dict={str(i):0 for i in range(1,this_month_endtime.day+1)}
            #print day_dict
            all_person[Issuing_person.objects.get(pk=i['issuing_person']).name]=OrderedDict(sorted(day_dict.items(),key=lambda k:int(k[0])))
#    print all_person
    for i in this_order_data:
        all_person[Issuing_person.objects.get(pk=i['issuing_person']).name][str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
    return render(request,'issuing_person_reporter.html',{'alldata':all_person,'data':day_money,'starttime':starttime,'endtime':endtime,'issuing_person':issuing_person})
