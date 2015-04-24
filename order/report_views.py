#coding=utf-8
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from role.models import *
from django.shortcuts import render
from models import *
from django.db.models import Count,Sum
import datetime
from django.utils.translation import  gettext as _
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
                try:
                    day_money[i['day']]=Product.objects.get(pk=i['product']).price
                except:
                    day_money[i['day']]=0
            else:
                try:
                    day_money[i['day']]+=Product.objects.get(pk=i['product']).price
                except:
                    day_money[i['day']]+=0
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
    if this_order_data:
        this_day_money=OrderedDict()
        for i in range(1,this_month_endtime.day+1):
                #this_day_money[this_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
            this_day_money[str(i)]=0
            #print this_day_money
        for i in this_order_data:
            try:
                this_day_money[str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
            except:
                this_day_money[str(int(i['day'][-2:]))]+=0
    else:
        this_day_money=OrderedDict()
        for i in range(1,this_month_endtime.day+1):
                #this_day_money[this_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
            this_day_money[str(i)]=0
    last_order_data=Order.objects.filter(jointime__gte=last_format_starttime).filter(jointime__lte=last_format_endtime).extra({'day':'date(jointime)'}).values('day','product')
    last_day_money=OrderedDict()
    if last_order_data:
        for i in range(1,last_month_endtime.day+1):
                #last_day_money[last_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
            last_day_money[str(i)]=0
        for i in last_order_data:
            try:
                last_day_money[str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
            except:
                last_day_money+=0
    else:
        for i in range(1,last_month_endtime.day+1):
                #last_day_money[last_month_endtime.replace(day=i).strftime('%Y-%m-%d')]=0
            last_day_money[str(i)]=0
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
                try:
                    day_money[i['day']]=Product.objects.get(pk=i['product']).price
                except:
                    day_money[i['day']]=0
            else:
                try:
                    day_money[i['day']]+=Product.objects.get(pk=i['product']).price
                except:
                    day_money[i['day']]+=0
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
        try:
            staff=Issuing_person.objects.get(pk=i['issuing_person']).name
        except:
            continue
        if staff in all_person:
            pass
        else:
            #day_dict={str(i):0 for i in range(1,this_month_endtime.day+1)}
            #print day_dict
            all_person[Issuing_person.objects.get(pk=i['issuing_person']).name]=OrderedDict(sorted(day_dict.items(),key=lambda k:int(k[0])))
#    print all_person
    for i in this_order_data:
        try:
            staff=Issuing_person.objects.get(pk=i['issuing_person']).name
        except:
            continue
        try:
            all_person[Issuing_person.objects.get(pk=i['issuing_person']).name][str(int(i['day'][-2:]))]+=Product.objects.get(pk=i['product']).price
        except:
            all_person[Issuing_person.objects.get(pk=i['issuing_person']).name][str(int(i['day'][-2:]))]+=0
    return render(request,'issuing_person_reporter.html',{'alldata':all_person,'data':day_money,'starttime':starttime,'endtime':endtime,'issuing_person':issuing_person})

@admin_required(login_url="/login/")
def person_sale_report(request):
    if request.method=="POST":
        group_name=request.POST.get("group_name")
        server=request.POST.get("server")
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        if group_name:
            order=Order_all_info.objects.filter(user_group_name=group_name)
        else:
            order=Order_all_info.objects.all()
        if server:
            order=order.filter(user_firstname=server)
        if starttime:
            order=order.filter(jointime__gte=starttime)
        if endtime:
            order=order.filter(jointime__lte=endtime)
        order_list=[]
        order_dict={}
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()
        user_list=order.exclude(user_username=None).values_list('user_username','user_group_name','user_first_name').distinct()
        for i in user_list:
            order_dict['order_quantity']=order.filter(user_username=i[0]).count()
            order_dict['check_failed']=order.filter(user_username=i[0]).filter(state_level=1).count()
            order_dict['check_success']=order.filter(user_username=i[0]).filter(state_level__gte=2).count()
            order_dict['order_success']=order.filter(user_username=i[0]).filter(Q(state_level=3)&Q(state_name=_("已签收"))).count()
            order_dict['order_question']=order.filter(user_username=i[0]).filter(Q(state_level=3)&~Q(state_name=_("已签收"))).count()
            order_dict['group']=i[1]
            order_dict['firstname']=i[2]
            order_list.append(order_dict)
            order_dict={}

    else:
        order_list=[]
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()
        user_list=Order_all_info.objects.exclude(user_username=None).values_list('user_username').distinct()

    return render(request,'person_sale_report.html',{'groups':group_list,'users':user_list,'order':order_list})

@admin_required(login_url="/login/")
def team_sale_report(request):
    if request.method=="POST":
        group_name=request.POST.get("group_name")
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        if group_name:
            order=Order_all_info.objects.filter(user_group_name=group_name)
        else:
            order=Order_all_info.objects.all()
        if starttime:
            order=order.filter(jointime__gte=starttime)
        if endtime:
            order=order.filter(jointime__lte=endtime)
        order_list=[]
        order_dict={}
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()

        for i in group_list:
            order_dict['order_quantity']=order.filter(user_group_name=i[0]).count()
            order_dict['check_failed']=order.filter(user_group_name=i[0]).filter(state_level=1).count()
            order_dict['check_success']=order.filter(user_group_name=i[0]).filter(state_level__gte=2).count()
            order_dict['order_success']=order.filter(user_group_name=i[0]).filter(Q(state_level=3)&Q(state_name=_("已签收"))).count()
            order_dict['order_question']=order.filter(user_group_name=i[0]).filter(Q(state_level=3)&~Q(state_name=_("已签收"))).count()
            order_dict['group']=i[0]
            order_list.append(order_dict)
            order_dict={}

    else:
        order_list=[]
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()

    return render(request,'team_sale_report.html',{'groups':group_list,'order':order_list})
@admin_required(login_url='/login/')
def order_success_report(request):
    if request.method=="POST":
        group_name=request.POST.get("group_name")
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        if group_name:
            order=Order_all_info.objects.filter(user_group_name=group_name)
        else:
            order=Order_all_info.objects.all()
        if starttime:
            order=order.filter(jointime__gte=starttime)
        if endtime:
            order=order.filter(jointime__lte=endtime)
        order_list=[]
        order_dict={}
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()

        for i in group_list:
            order_dict['success_quantity']=order.filter(user_group_name=i[0]).filter(Q(state_level=3)&Q(state_name=_("已签收"))).count()
            order_dict['success_money']=order.filter(user_group_name=i[0]).filter(Q(state_level=3)&Q(state_name=_("已签收")
            )).aggregate(money=Sum('product_price'))['money']
            order_dict['group']=i[0]
            order_list.append(order_dict)
            order_dict={}

    else:
        order_list=[]
        group_list=Order_all_info.objects.exclude(user_group_name=None).values_list('user_group_name').distinct()

    return render(request,'order_success_report.html',{'groups':group_list,'order':order_list})
