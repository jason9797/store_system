#coding=utf-8
from django.db import models
from django.contrib.auth.models import User,Group
from django.utils.translation import gettext as _
# Create your models here.
#from simple_history.models import HistoricalRecords
from order.models import *
from django.db.models import *
import datetime
from django.contrib.auth.models import User
#job_choices = (
#    (0, _("service")),
#    (1, _("Storekeeper")),
#)

class UserProfile(models.Model):
    '''
    用户表
    '''
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.SET_NULL)
    #role = models.IntegerField(choices=job_choices, default=0)
    role = models.ForeignKey('Role',blank=True,null=True,on_delete=models.SET_NULL)
    #history = HistoricalRecords()
    class Meta:
        verbose_name='用户角色关系'
    def __unicode__(self):
        return '%s-%s' % (self.user.username,self.role.name)

class Role(models.Model):
    name = models.CharField('名称',max_length=50)
    #history = HistoricalRecords()
    class Meta:
        verbose_name='角色'
    def __unicode__(self):
        return '%s'%self.name

class Issuing_person(models.Model):
    '''
    出单人
    '''
    name = models.CharField('名称',max_length=50)
    #history = HistoricalRecords()
    class Meta:
        verbose_name='出单人'
    def __unicode__(self):
        return '%s'%self.name
        
class User_goal(models.Model):
    user=models.ForeignKey(User,verbose_name='用户')
    goal_quantity=models.IntegerField(verbose_name="目标量",null=True,blank=True)
    goal_money=models.DecimalField(verbose_name="目标成交额",max_digits=7, decimal_places=2,default=0,null=True,blank=True)
    goal_chosen=models.BooleanField(verbose_name="0:出单量,1:目标额",default=0)


    def __unincode__(self):
        if self.goal_chosen:
            return '%s-%s'%(self.user.first_name,self.goal_money)
        else:
            return '%s-%s'%(self.user.first_name,self.goal_quantity)

class Issuing_person_cut(models.Model):
    issuing_person=models.ForeignKey(Issuing_person,verbose_name="出单人")
    cut_percentage=models.DecimalField(verbose_name="提成系数",max_digits=2, decimal_places=2,default=0,null=True,blank=True)
    jointime=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s-%s'%(self.issuing_person,self.cut_percentage)

class Server_cut(models.Model):
    server=models.ForeignKey(User,verbose_name="客服")
    cut_percentage=models.DecimalField(verbose_name="提成系数",max_digits=2, decimal_places=2,default=0,null=True,blank=True)
    jointime=models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return '%s-%s'%(self.server,self.cut_percentage)


def get_group_name(self):
    try:
        name=self.groups.all()[0].name
    except:
        name=''
    return name

def get_this_today(self):
    today=datetime.date.today()
    if self.is_superuser:
        today_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__is_superuser=False))&Q(jointime__gte=today))
    else:
        if self.id in [i[0] for i in Customer.objects.filter(user__isnull=False).values_list("user").distinct()]:
            today_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user=self))&Q(jointime__gte=today))
        else:
            return (0,0)
    this_day_quantity=today_order.count()
    this_day_money=sum([i.product.price for i in today_order])
    return (this_day_money,this_day_quantity)
def get_this_week(self):
    week_monday=datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday())
    if self.is_superuser:
        this_week_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__is_superuser=False))&Q(jointime__gte=week_monday))
    else:
        if self.id in [i[0] for i in Customer.objects.filter(user__isnull=False).values_list("user").distinct()]:
            this_week_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user=self))&Q(jointime__gte=week_monday))
        else:
            return (0,0)
    this_week_quantity=this_week_order.count()
    this_week_money=sum([i.product.price for i in this_week_order])
    return (this_week_money,this_week_quantity)
def get_this_month(self):
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    if self.is_superuser:
        this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__is_superuser=False))&Q(jointime__gte=this_month_start))
    else:
        if self.id in [i[0] for i in Customer.objects.filter(user__isnull=False).values_list("user").distinct()]:
            this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user=self))&Q(jointime__gte=this_month_start))
        else:
            return (0,0)
    this_month_quantity=this_month_order.count()
    this_month_money=sum([i.product.price for i in this_month_order])
    return (this_month_money,this_month_quantity)

def get_person_goal(self):
    try:
        goal=User_goal.objects.get(user=self)
    except:
        goal=0
    return goal


def get_person_cut(self):
    try:
        cut=Server_cut.objects.get(server=self)
    except:
        cut=0
    return cut
def get_order_success(self):
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    if self.is_superuser:
        this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__is_superuser=False))&Q(jointime__gte=this_month_start)).count()
        this_month_success=Order.objects.filter(Q(customer__in=Customer.objects.filter(
            user__is_superuser=False))&Q(jointime__gte=this_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    else:
        this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user=self))&Q(jointime__gte=this_month_start)).count()
        this_month_success=Order.objects.filter(Q(customer__in=Customer.objects.filter(
            user=self))&Q(jointime__gte=this_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(this_month_success) / float(this_month_order)) * 100)
    except:
        success_per=0
    return success_per

def get_team_goal(self):
    team_user=self.groups.all()[0].user_set.all()
    goal_money=User_goal.objects.filter(user__in=team_user).aggregate(Sum('goal_money'))['goal_money__sum']
    return goal_money

def get_team_order(self):
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    team_user=self.groups.all()[0].user_set.all()
    team_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__in=team_user))&Q(jointime__gte=this_month_start))
    team_month_money=sum([i.product.price for i in team_month_order])
    return team_month_money

def get_team_order_success(self):
    team_user=self.groups.all()[0].user_set.all()
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__in=team_user))&Q(jointime__gte=this_month_start)).count()
    this_month_success=Order.objects.filter(Q(customer__in=Customer.objects.filter(
            user=team_user))&Q(jointime__gte=this_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(this_month_success) / float(this_month_order)) * 100)
    except:
        success_per=0
    return success_per

def this_day_rank(self):
    today=datetime.date.today()
    team_user=self.groups.all()[0].user_set.all()
    rank_list=[]
    for i in team_user:
        this_day_order=Order.objects.filter(Q(
        customer__in=Customer.objects.filter(user=i))&Q(
        jointime__gte=today))
        if this_day_order:
            this_day_order=this_day_order.aggregate(sum_order=Sum("product__price"))
            rank_list.append((i,this_day_order['sum_order']))
        else:
            rank_list.append((i,0))

    rank_list=sorted(rank_list,key=(lambda x:x[1]),reverse=True)
    for i in rank_list:
        if self in i:
            return rank_list.index(i)+1,i[1]

def this_week_rank(self):
    week_monday=datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday())
    team_user=self.groups.all()[0].user_set.all()
    rank_list=[]
    for i in team_user:
        this_week_order=Order.objects.filter(Q(
        customer__in=Customer.objects.filter(user=i))&Q(
        jointime__gte=week_monday))
        if this_week_order:
            this_week_order=this_week_order.aggregate(sum_order=Sum("product__price"))
            rank_list.append((i,this_week_order['sum_order']))
        else:
            rank_list.append((i,0))
    rank_list=sorted(rank_list,key=(lambda x:x[1]),reverse=True)
    for i in rank_list:
        if self in i:
            return rank_list.index(i)+1,i[1]
        
def this_month_rank(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    team_user=self.groups.all()[0].user_set.all()
    rank_list=[]
    for i in team_user:
        this_month_order=Order.objects.filter(Q(
        customer__in=Customer.objects.filter(user=i))&Q(
        jointime__gte=month_start))
        if this_month_order:
            this_month_order=this_month_order.aggregate(sum_order=Sum("product__price"))
            rank_list.append((i,this_month_order['sum_order']))
        else:
            rank_list.append((i,0))
    rank_list=sorted(rank_list,key=(lambda x:x[1]),reverse=True)
    for i in rank_list:
        if self in i:
            return rank_list.index(i)+1,i[1]

def person_quantity_rank(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(
        jointime__gte=month_start))
    quantity_person=this_month_order.values("customer__user").annotate(quantity=Count("customer__user")).order_by("-quantity")
    quantity_person=quantity_person.exclude(customer__user=None)[:5]
    for i in quantity_person:
        if i['customer__user']:
            i['customer__user']=User.objects.get(id=i['customer__user'])
    return quantity_person

def person_money_rank(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(
        jointime__gte=month_start))

    money_person=this_month_order.values("customer__user").annotate(money=Sum("product__price")).order_by("-money")
    money_person=money_person.exclude(customer__user=None)[:5]
    for i in money_person:
        if i['customer__user']:
            i['customer__user']=User.objects.get(id=i['customer__user'])
    return money_person

def get_team_rank(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    groups=Group.objects.all()
    groups_list=[]
    for i in groups:
        this_month_order=Order.objects.filter(Q(customer__in=Customer.objects.filter(user__in=i.user_set.all()))&Q(jointime__gte=month_start))
        if this_month_order:
            total_money=this_month_order.aggregate(money=Sum("product__price"))['money']
            groups_list.append({"name":i.name,"money":total_money})

    groups_list=sorted(groups_list,key=(lambda x:x['money']),reverse=True)
    return groups_list

def get_failed_order(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(state=Order_State.objects.filter(~Q(name="已签收")&Q(level__gte=3)))&Q(jointime__gte=month_start)).order_by("-jointime")
    return this_month_order

def get_no_approval_order(self):
    month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(state=Order_State.objects.filter(level=1))&Q(jointime__gte=month_start)).order_by("-jointime")
    return this_month_order

def get_this_week_success(self):
    week_monday=datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday())
    this_week_order=Order.objects.filter(Q(jointime__gte=week_monday)).count()
    this_week_success=Order.objects.filter(Q(jointime__gte=week_monday)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(this_week_success) / float(this_week_order)) * 100)
    except:
        success_per=0
    return success_per

def get_last_week_success(self):
    last_week_monday=datetime.date.today()-datetime.timedelta(days=(datetime.date.today().weekday()+7))
    last_week_order=Order.objects.filter(Q(jointime__gte=last_week_monday)).count()
    last_week_success=Order.objects.filter(Q(jointime__gte=last_week_monday)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(last_week_success) / float(last_week_order)) * 100)
    except:
        success_per=0
    return success_per

def get_this_month_success(self):
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order=Order.objects.filter(Q(jointime__gte=this_month_start)).count()
    this_month_success=Order.objects.filter(Q(jointime__gte=this_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(this_month_success) / float(this_month_order)) * 100)
    except:
        success_per=0
    return success_per

def get_last_month_success(self):
    last_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    last_month_order=Order.objects.filter(Q(jointime__gte=last_month_start)).count()
    last_month_success=Order.objects.filter(Q(jointime__gte=last_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    try:
        success_per="%.2f%%" %((float(last_month_success) / float(last_month_order)) * 100)
    except:
        success_per=0
    return success_per

def get_week_order(self):
    week_monday=datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday())
    this_week_order_count=Order.objects.filter(Q(jointime__gte=week_monday)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    this_week_order_money=Order.objects.filter(Q(jointime__gte=week_monday)&Q(
        state=Order_State.objects.get(name=_('已签收')))).aggregate(Sum('product__price'))['product__price__sum']
    if not this_week_order_money:
        this_week_order_money=0
    return this_week_order_count,this_week_order_money

def get_month_order(self):
    this_month_start=datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    this_month_order_count=Order.objects.filter(Q(jointime__gte=this_month_start)&Q(state=Order_State.objects.get(name=_('已签收')))).count()
    this_month_order_money=Order.objects.filter(Q(jointime__gte=this_month_start)&Q(
        state=Order_State.objects.get(name=_('已签收')))).aggregate(Sum('product__price'))['product__price__sum']
    if not this_month_order_money:
        this_month_order_money=0
    return this_month_order_count,this_month_order_money






User.add_to_class("get_group_name",get_group_name)
User.add_to_class("get_this_today",get_this_today)
User.add_to_class("get_this_week",get_this_week)
User.add_to_class("get_this_month",get_this_month)
User.add_to_class("get_person_goal",get_person_goal)
User.add_to_class("get_person_cut",get_person_cut)
User.add_to_class("get_order_success",get_order_success)
User.add_to_class("get_team_goal",get_team_goal)
User.add_to_class("get_team_order",get_team_order)
User.add_to_class("get_team_order_success",get_team_order_success)
User.add_to_class("this_day_rank",this_day_rank)
User.add_to_class("this_week_rank",this_week_rank)
User.add_to_class("this_month_rank",this_month_rank)
User.add_to_class("person_quantity_rank",person_quantity_rank)
User.add_to_class("person_money_rank",person_money_rank)
User.add_to_class("get_team_rank",get_team_rank)
User.add_to_class("get_failed_order",get_failed_order)
User.add_to_class("get_no_approval_order",get_no_approval_order)
User.add_to_class("get_this_week_success",get_this_week_success)
User.add_to_class("get_last_week_success",get_last_week_success)
User.add_to_class("get_this_month_success",get_this_month_success)
User.add_to_class("get_last_month_success",get_last_month_success)
User.add_to_class("get_week_order",get_week_order)
User.add_to_class("get_month_order",get_month_order)
