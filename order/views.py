#coding=utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core import serializers
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from role.models import *
from role.forms import *
import math
from stock.forms import *
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

User.is_server=is_server

def server_required(login_url=None):
    return user_passes_test(lambda u:u.is_server(),login_url=login_url)

@server_required(login_url='/login')
def order_add(request):
    if request.method=="POST":
        order_form=OrderForm(request.POST)
        if order_form.is_valid():
            data=order_form.cleaned_data
            # if request.GET.get("id"):
            #     order=Order.objects.get(pk=request.GET.get('id'))
            #     order.delivery_no=data['delivery_no']
            #     order.fact_money=data['fact_money']
            #     order.customer=data['customer']
            #     order.issuing_person=data['issuing_person']
            #     order.product=data['product']
            #     order.order_state=data['state']
            #     order.save()
            # else:
            delivery_no=data['delivery_no']
            fact_money=data['fact_money']
            customer=data['customer']
            issuing_person=data['issuing_person']
            product=data['product']
            order_state=data['state']
            order=Order(delivery_no=delivery_no,fact_money=fact_money,customer=customer,issuing_person=issuing_person,
                    product=product,state=order_state)
            order.save()
            return HttpResponseRedirect("/order/order/add")
        #else:
        #    print order_form.errors
    else:
        # if request.GET.get('id'):
        #     order_form=OrderForm(model_to_dict(Order.objects.get(pk=request.GET.get('id'))))
        # else:
        order_form=OrderForm()

    # order_data=Order.objects.all()
    # customer_form=CustomerForm()
    # issuing_person_form=Issuing_personForm()
    # product_form=ProductForm()
    # order_state_form=Order_StateForm()
    form_list={
               # 'order_data':order_data,
               'order_form':order_form,
               # 'customer_form':customer_form,
               # 'issuing_person_form':issuing_person_form,
               # 'product_form':product_form,
               # 'order_state_form':order_state_form,
        }
    return render(request,'order_add.html',form_list)
@server_required(login_url='/login')
def order_edit(request):
    if request.method=="POST":
        print request.POST
        name=request.POST.get('name')
        value=request.POST.get('value')
        if name=='customer':
            value=Customer.objects.get(name=value)
        if name=="issuing_person":
            value=Issuing_person.objects.get(name=value)
        if name=='product':
            value=Product.objects.get(name=value)
        if name=='state':
            value=Order_State.objects.get(name=value)
            print value
        info_dict={'%s'%name:value}
        order=Order.objects.filter(pk=request.POST.get("pk"))
        order.update(**info_dict)
        return HttpResponse('success')

@server_required(login_url='/login')
def order_home_remove(request):
    order_id=request.GET.get("id")
    order=Order.objects.get(pk=order_id)
    order.delete()
    return HttpResponseRedirect("/order/order/info/")

@server_required(login_url='/login')
def order_customer_add(request):
    if request.method=="POST":
        customer_form=CustomerForm(request.POST)
        if customer_form.is_valid():
            data=customer_form.cleaned_data
            name=data['name']
            sex=data['sex']
            level=data['level']
            issuing_person=data['issuing_person']
            user=data['user'].user
            customer=Customer(name=name,sex=sex,level=level,issuing_person=issuing_person,user=user)
            customer.save()
            return HttpResponseRedirect("/order/customer")
    else:
        #if request.GET.get("id"):
        #    customer_form=CustomerForm(model_to_dict(Customer.objects.get(pk=request.GET.get("id"))))
        #else:
        customer_form=CustomerForm()
    #customer_data=Customer.objects.all()
    level_form=Customer_LevelForm()
    form_list={
               #'customer_data':customer_data,
               'customer_form':customer_form,
               'customer_level':level_form,
               }
    return render(request,'order_customer_add.html',form_list)

@server_required(login_url='/login')
def order_customer_remove(request):
    customer_id=request.GET.get("id")
    customer=Customer.objects.get(pk=customer_id)
    customer.delete()
    return HttpResponseRedirect("/order/customer")

@server_required(login_url='/login')
def order_customer_level(request):
    if request.method=="POST":
        customer_level_form=Customer_LevelForm(request.POST)
        if customer_level_form.is_valid():
            data=customer_level_form.cleaned_data
            if request.GET.get("id"):
                customer_level=Customer_Level.objects.get(pk=request.GET.get('id'))
                customer_level.level=data['level']
                customer_level.save()
            else:
                level=data['level']
                customer_level=Customer_Level(level=level)
                customer_level.save()
            return HttpResponseRedirect("/order/customer_level")
    else:
        if request.GET.get("id"):
            customer_level_form=Customer_LevelForm(model_to_dict(Customer_Level.objects.get(pk=request.GET.get("id"))))
        else:
            customer_level_form=Customer_LevelForm()
    customer_level_data=Customer_Level.objects.all()
    form_list={
               'customer_level_data':customer_level_data,
               'customer_level_form':customer_level_form,
               }
    return render(request,'order_customer_level.html',form_list)

@server_required(login_url='/login')
def order_customer_level_remove(request):
    level_id=request.GET.get("id")
    level=Customer_Level.objects.get(pk=level_id)
    level.delete()
    return HttpResponseRedirect("/order/customer_level")

@server_required(login_url='/login')
def order_contact(request):
    if request.method=="POST":
        contact_form=Contact_infoForm(request.POST)
        if contact_form.is_valid():
            data=contact_form.cleaned_data
            if request.GET.get("id"):
                contact=Contact_info.objects.get(pk=request.GET.get('id'))
                contact.address=data['address']
                contact.phone_number=data['phone_number']
                contact.customer=data['customer']
                contact.save()
            else:
                address=data['address']
                phone_number=data['phone_number']
                customer=data['customer']
                contact=Contact_info(address=address,phone_number=phone_number,customer=customer)
                contact.save()
            return HttpResponseRedirect("/order/contact")
    else:
        if request.GET.get('id'):
            contact_form=Contact_infoForm(model_to_dict(Contact_info.objects.get(pk=request.GET.get('id'))))
        else:
            contact_form=Contact_infoForm()
    contact_data=Contact_info.objects.all()
    customer_form=CustomerForm()
    form_list={
               'contact_data':contact_data,
               'customer_form':customer_form,
               'contact_form':contact_form
               }
    return render(request,'order_contact.html',form_list)
@server_required(login_url='/login')
def order_contact_remove(request):
    contact_id=request.GET.get("id")
    contact=Contact_info.objects.get(pk=contact_id)
    contact.delete()
    return HttpResponseRedirect("/order/contact")

@server_required(login_url='/login')
def order_state(request):
    if request.method=="POST":
        state_form=Order_StateForm(request.POST)
        if state_form.is_valid():
            data=state_form.cleaned_data
            if request.GET.get("id"):
                state=Order_State.objects.get(pk=request.GET.get('id'))
                state.name=data['name']
                state.save()
            else:
                name=data['name']
                state=Order_State(name=name)
                state.save()
            return HttpResponseRedirect("/order/state")
    else:
        if request.GET.get('id'):
            state_form=Order_StateForm(model_to_dict(Order_State.objects.get(pk=request.GET.get('id'))))
        else:
            state_form=Order_StateForm()
    state_data=Order_State.objects.all()
    form_list={
               'state_data':state_data,
               'state_form':state_form
               }
    return render(request,'order_state.html',form_list)
@server_required(login_url='/login')
def order_state_remove(request):
    state_id=request.GET.get("id")
    state=Order_State.objects.get(pk=state_id)
    state.delete()
    return HttpResponseRedirect("/order/state")

@server_required(login_url='/login')
def order_stock_product(request):
    if request.method=="POST":
        stock_product_form=Stock_ProductForm(request.POST)
        if stock_product_form.is_valid():
            data=stock_product_form.cleaned_data
            if request.GET.get("id"):
                stock_product=Stock_Product.objects.get(pk=request.GET.get('id'))
                stock_product.quantity-=data['quantity']
                stock_product.delivery_bill=data['delivery_bill']
                stock_product.product=data['product']
                stock_product.stock=data['stock']
                stock_product.save()
            else:
                quantity=data['quantity']
                delivery=data['delivery_bill']
                product=data['product']
                stock=data['stock']
                stock_product=Stock_Product(quantity=quantity,delivery_bill=delivery,product=product,stock=stock)
                stock_product.save()
            return HttpResponseRedirect("/order/stock_product")
    else:
        if request.GET.get('id'):
            stock_product_form=Stock_ProductForm(model_to_dict(Stock_Product.objects.get(pk=request.GET.get('id'))))
        else:
            stock_product_form=Stock_ProductForm()
    stock_product_data=Stock_Product.objects.all()
    form_list={
               'stock_product_data':stock_product_data,
               'stock_product_form':stock_product_form,
               'stock_form':StockForm
               }
    return render(request,'order_stock_product.html',form_list)
@server_required(login_url='/login')
def order_stock_product_remove(request):
    stock_product_id=request.GET.get("id")
    stock_product=Stock_Product.objects.get(pk=stock_product_id)
    stock_product.delete()
    return HttpResponseRedirect("/order/stock_product")

@server_required(login_url='/login')
def order_product_add(request):
    if request.method=="POST":
        product_form=ProductForm(request.POST)
        if product_form.is_valid():
            data=product_form.cleaned_data
            name=data['name']
            price=data['price']
            delivery_type=data['delivery_type']
            product=Product(name=name,price=price,delivery_type=delivery_type)
            product.save()
            return HttpResponseRedirect("/order/product")

    else:
        product_form=ProductForm()
    form_list={
               'product_form':product_form,
               }
    return render(request,'order_product_add.html',form_list)
@server_required(login_url='/login')
def order_product_edit(request):
    if request.method=="POST":
        print request.POST
        name=request.POST.get('name')
        if name=='price':
            value=float(request.POST.get('value'))
        else:
            value=request.POST.get('value')
        info_dict={'%s'%name:value}
        product=Product.objects.filter(pk=request.POST.get("pk"))
        product.update(**info_dict)
        return HttpResponse('success')
@server_required(login_url='/login')
def order_product_remove(request):
    product_id=request.GET.get("id")
    product=Product.objects.get(pk=product_id)
    product.delete()
    return HttpResponseRedirect("/order/product")

@server_required(login_url='/login')
def order_issuing_person(request):
    if request.method=="POST":
        issuing_person_form=Issuing_personForm(request.POST)
        if issuing_person_form.is_valid():
            data=issuing_person_form.cleaned_data
            if request.GET.get("id"):
                issuing_person=Issuing_person.objects.get(pk=request.GET.get('id'))
                issuing_person.name=data['name']
                issuing_person.save()
            else:
                name=data['name']
                person=Issuing_person(name=name)
                person.save()
            return HttpResponseRedirect("/order/issuing_person")
    else:
        if request.GET.get('id'):
            issuing_person_form=Issuing_personForm(model_to_dict(Issuing_person.objects.get(pk=request.GET.get('id'))))
        else:
            issuing_person_form=Issuing_personForm()
    issuing_person_data=Issuing_person.objects.all()
    form_list={
               'issuing_person_data':issuing_person_data,
               'issuing_person_form':issuing_person_form
               }
    return render(request,'order_issuing_person.html',form_list)
@server_required(login_url='/login')
def order_issuing_person_remove(request):
    person_id=request.GET.get("id")
    person=Issuing_person.objects.get(pk=person_id)
    person.delete()
    return HttpResponseRedirect("/order/issuing_person")

@server_required(login_url='/login')
def my_customer(request):
    if request.method=='POST':
        name=request.POST.get('name')
        filter_dict={}
        initial={}
        if name:
            customer=Customer.objects.filter(name__contains=name)
            filter_dict['name']=name
        else:
            customer=Customer.objects.all()
        level=request.POST.get('level')
        if level:
            customer=customer.filter(level=Customer_Level.objects.get(pk=level))
            initial['level']=Customer_Level.objects.get(pk=level)
        sex=request.POST.get('sex')
        if sex:
            customer=customer.filter(sex=eval(sex))
            filter_dict['sex']=eval(sex)
        server=request.POST.get('user')
        #print server
        #print customer
        if request.user.is_superuser:
            if server:
                #print server
                #print customer
                customer=customer.filter(user=UserProfile.objects.get(pk=int(server)).user)
                initial['user']=UserProfile.objects.get(pk=int(server))
            else:
                customer=customer.filter(user__in=UserProfile.objects.filter(role=Role.objects.get(name=u'客服')).values('user'))
                #initial['user']=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        else:
            customer=customer.filter(user=request.user)
            initial['user']=UserProfile.objects.get(user=request.user)
            #print UserProfile.objects.get(user=request.user)


        issuing_person=request.POST.get('issuing_person')
        if issuing_person:
            try:
                customer=customer.filter(issuing_person=Issuing_person.objects.get(pk=int(issuing_person)))
                initial['issuing_person']=Issuing_person.objects.get(pk=int(issuing_person))
            except:
                return HttpResponseRedirect('/order/my_customer')

        starttime=request.POST.get('starttime')
        if starttime:
            customer=customer.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            customer=customer.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=CustomerForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(customer))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            #print start_page,end_page
            #total_page=math.ceil(float(len(customer))/5)
            #customer_json=serializers.serialize('json',customer[start_page:end_page])
            #print customer_json
            customer=customer[start_page:end_page]
            #return HttpResponse(customer.query)
            level=Customer_Level.objects.all()
            if request.user.is_superuser:
                userlist=User.objects.all()
            else:
                userlist=User.objects.filter(pk=request.user.id)
            issuing_person=Issuing_person.objects.all()
            return render(request,'my_customer_pagination.html',{'customer':customer,'userlist':userlist,
                                                              'level':level,'issuing_person':issuing_person
                                              })

        else:
            #print customer
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(customer))/5))
            customer=customer[:end_page]
            #return HttpResponse(customer.query)
            #print total_page
            page=1
        #print customer
        # customer=Customer.objects.filter(name__contains=name,level=Customer_Level.objects.get(pk=level),
        #      sex=sex,user=User.objects.get(pk=server),issuing_person=Issuing_person.objects.get(pk=issuing_person),
        #  jointime__gte=starttime,jointime__lte=endtime)
    else:
        form=CustomerForm()
        if request.user.is_superuser:
            server=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        else:
            server=UserProfile.objects.filter(user=request.user)
        if request.user.is_superuser:
            form.fields['user'].queryset=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        else:
            form.fields['user'].queryset=UserProfile.objects.filter(user=request.user)
        customer=[]
        filter_dict={}
        total_page=0
        page=0
    level=Customer_Level.objects.all()
    if request.user.is_superuser:
        userlist=User.objects.filter(id__in=UserProfile.objects.filter(role=Role.objects.get(name=u'客服')).values('user'))
    else:
        userlist=User.objects.filter(pk=request.user.id)
    issuing_person=Issuing_person.objects.all()
    info={"server":server,'form':form,'customer':customer,'filter':filter_dict,
        'total_page':total_page,'current_page':page,'level':level,'issuing_person':issuing_person,'userlist':userlist}
    return render(request,'my_customer.html',info)
@server_required(login_url='/login')
def order_customer_edit(request):
    if request.method=="POST":
        #print request.POST
        name=request.POST.get('name')
        try:
            value=eval(request.POST.get('value[]'))
        except:
            value=request.POST.get('value')
        if name=='user':
            value=User.objects.get(username=value)
        if name=='issuing_person':
            value=Issuing_person.objects.get(name=value)
        info_dict={'%s'%name:value}
        customer=Customer.objects.filter(pk=request.POST.get("pk"))
        customer.update(**info_dict)
        return HttpResponse('success')
@server_required(login_url='/login')
def order_customer(request):
    if request.method=='POST':
        name=request.POST.get('name')
        filter_dict={}
        initial={}
        if name:
            customer=Customer.objects.filter(name__contains=name)
            filter_dict['name']=name
        else:
            customer=Customer.objects.all()
        level=request.POST.get('level')
        if level:
            customer=customer.filter(level=Customer_Level.objects.get(pk=level))
            initial['level']=Customer_Level.objects.get(pk=level)
        sex=request.POST.get('sex')
        if sex:
            customer=customer.filter(sex=eval(sex))
            filter_dict['sex']=eval(sex)
        server=request.POST.get('user')
        if request.user.is_superuser:
            if server:
                customer=customer.filter(user=UserProfile.objects.get(pk=int(server)).user)
                initial['user']=UserProfile.objects.get(pk=int(server))
            else:
                customer=customer.filter(user__in=UserProfile.objects.filter(role=Role.objects.get(name=u'客服')).values('user'))
                #initial['user']=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        else:
            customer=customer.filter(user=request.user)
            initial['user']=UserProfile.objects.get(user=request.user)
        issuing_person=request.POST.get('issuing_person')
        if issuing_person:
            try:
                customer=customer.filter(issuing_person=Issuing_person.objects.get(pk=int(issuing_person)))
                initial['issuing_person']=Issuing_person.objects.get(pk=int(issuing_person))
            except:
                return HttpResponseRedirect('/order/customer')

        starttime=request.POST.get('starttime')
        if starttime:
            customer=customer.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            customer=customer.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=CustomerForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(customer))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            customer=customer[start_page:end_page]
            return render(request,'customer_pagination.html',{'customer':customer
                                              })

        else:
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(customer))/5))
            customer=customer[:end_page]
            page=1
    else:
        form=CustomerForm()
        server=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        form.fields['user'].queryset=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        customer=[]
        filter_dict={}
        total_page=0
        page=0
    info={"server":server,'form':form,'customer':customer,'filter':filter_dict,
        'total_page':total_page,'current_page':page}
    return render(request,'order_customer.html',info)
@server_required(login_url='/login')
def order_product(request):
    if request.method=='POST':
        name=request.POST.get('name')
        filter_dict={}
        initial={}
        if name:
            product=Product.objects.filter(name__contains=name)
            filter_dict['name']=name
        else:
            product=Product.objects.all()
        starttime=request.POST.get('starttime')
        if starttime:
            product=product.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            product=product.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=ProductForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(product))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            product=product[start_page:end_page]
            return render(request,'product_pagination.html',{'product':product
                                              })

        else:
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(product))/5))
            product=product[:end_page]
            page=1
    else:
        form=ProductForm()
        product=[]
        filter_dict={}
        total_page=0
        page=0
    info={'form':form,'product':product,'filter':filter_dict,
        'total_page':total_page,'current_page':page}
    return render(request,'order_product.html',info)

@server_required(login_url='/login')
def order_info(request):
    if request.method=='POST':
        delivery_no=request.POST.get('delivery_no')
        filter_dict={}
        initial={}
        if delivery_no:
            order=Order.objects.filter(delivery_no__contains=delivery_no)
            filter_dict['delivery_no']=delivery_no
        else:
            order=Order.objects.all()
        fact_money=request.POST.get('fact_money')
        if fact_money:
            order=order.filter(fact_money=fact_money)
            filter_dict['fact_money']=fact_money
        customer=request.POST.get('customer')
        if customer:
            order=order.filter(customer=Customer.objects.get(pk=int(customer)))
            initial['customer']=Customer.objects.get(pk=int(customer))

        issuing_person=request.POST.get('issuing_person')
        if issuing_person:
            try:
                order=order.filter(issuing_person=Issuing_person.objects.get(pk=int(issuing_person)))
                initial['issuing_person']=Issuing_person.objects.get(pk=int(issuing_person))
            except:
                return HttpResponseRedirect('/order/order/info')
        product=request.POST.get('product')
        if product:
            try:
                order=order.filter(product=Product.objects.get(pk=int(product)))
                initial['product']=Product.objects.get(pk=int(product))
            except:
                return HttpResponseRedirect('/order/order/info')

        state=request.POST.get('state')
        if state:
            try:
                order=order.filter(state=Order_State.objects.get(pk=int(state)))
                initial['state']=Order_State.objects.get(pk=int(state))
            except:
                return HttpResponseRedirect('/order/order/info')

        starttime=request.POST.get('starttime')
        if starttime:
            customer=order.filter(jointime__gte=starttime)
            filter_dict['starttime']=starttime
        endtime=request.POST.get('endtime')
        if endtime:
            customer=order.filter(jointime__lte=endtime)
            filter_dict['endtime']=endtime
        form=OrderForm(initial)
        page=request.POST.get('page')
        if page:
            total_page=int(math.ceil(float(len(order))/5))
            if int(page)==1:
                start_page=0
                end_page=5
            else:
                start_page=5*(int(page)-1)
                end_page=5*int(page)
            order=order[start_page:end_page]
            state_list=Order_State.objects.all()
            product_list=Product.objects.all()
            customer_list=Customer.objects.all()
            issuing_person_list=Issuing_person.objects.all()
            return render(request,'order_pagination.html',{'order':order,'state':state_list,'product':product_list,
                                              'customer':customer_list,'issuing_person':issuing_person_list})

        else:
            start_page=0
            end_page=5
            total_page=int(math.ceil(float(len(order))/5))
            order=order[:end_page]
            page=1
    else:
        form=OrderForm()

        customer=[]
        filter_dict={}
        total_page=0
        page=0
        order=[]
    state_list=Order_State.objects.all()
    product_list=Product.objects.all()
    customer_list=Customer.objects.all()
    issuing_person_list=Issuing_person.objects.all()
    info={'form':form,'filter':filter_dict,'order':order,
        'total_page':total_page,'current_page':page,'state':state_list,'product':product_list,
                                              'customer':customer_list,'issuing_person':issuing_person_list}
    return render(request,'order_info.html',info)