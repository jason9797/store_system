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
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from role.models import *
from role.forms import *
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
def order_home(request):
    if request.method=="POST":
        order_form=OrderForm(request.POST)
        if order_form.is_valid():
            data=order_form.cleaned_data
            delivery_no=data['delivery_no']
            fact_money=data['fact_money']
            customer=data['customer']
            issuing_person=data['issuing_person']
            product=data['product']
            order_state=data['state']
            order=Order(delivery_no=delivery_no,fact_money=fact_money,customer=customer,issuing_person=issuing_person,
                    product=product,state=order_state)
            order.save()
            return HttpResponseRedirect("/order/home")
    else:
        order_data=Order.objects.all()
        if request.GET.get('id'):
            order_form=OrderForm(model_to_dict(Order.objects.get(pk=request.GET.get('id'))))
        else:
            order_form=OrderForm()
        customer_form=CustomerForm()
        issuing_person_form=Issuing_personForm()
        product_form=ProductForm()
        order_state_form=Order_StateForm()
        form_list={
               'order_data':order_data,
               'order_form':order_form,
               'customer_form':customer_form,
               'issuing_person_form':issuing_person_form,
               'product_form':product_form,
               'order_state_form':order_state_form
        }
        return render(request,'order_home.html',form_list)
@server_required(login_url='/login')
def order_home_remove(request):
    order_id=request.GET.get("id")
    order=Order.objects.get(pk=order_id)
    order.delete()
    return HttpResponseRedirect("/order/home")

@server_required(login_url='/login')
def order_customer(request):
    if request.method=="POST":
        customer_form=CustomerForm(request.POST)
        if customer_form.is_valid():
            data=customer_form.cleaned_data
            name=data['name']
            sex=data['sex']
            level=data['level']
            customer=Customer(name=name,sex=sex,level=level)
            customer.save()
            return HttpResponseRedirect("/order/customer")
    else:
        customer_data=Customer.objects.all()
        if request.GET.get("id"):
            customer_form=CustomerForm(model_to_dict(Customer.objects.get(pk=request.GET.get("id"))))
        else:
            customer_form=CustomerForm()
        level_form=Customer_LevelForm()
        form_list={
               'customer_data':customer_data,
               'customer_form':customer_form,
               'customer_level':level_form
               }
        return render(request,'order_customer.html',form_list)

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
            level=data['level']
            customer_level=Customer_Level(level=level)
            customer_level.save()
            return HttpResponseRedirect("/order/customer_level")
    else:
        customer_level_data=Customer_Level.objects.all()
        if request.GET.get("id"):
            customer_level_form=Customer_LevelForm(model_to_dict(Customer_Level.objects.get(pk=request.GET.get("id"))))
        else:
            customer_level_form=Customer_LevelForm()
        form_list={
               'customer_level_data':customer_level_data,
               'customer_level_form':customer_level_form
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
            address=data['address']
            phone_number=data['phone_number']
            customer=data['customer']
            contact=Contact_info(address=address,phone_number=phone_number,customer=customer)
            contact.save()
            return HttpResponseRedirect("/order/contact")
    else:
        contact_data=Contact_info.objects.all()
        if request.GET.get('id'):
            contact_form=Contact_infoForm(model_to_dict(Contact_info.objects.get(pk=request.GET.get('id'))))
        else:
            contact_form=Contact_infoForm()
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
            name=data['name']
            state=Order_State(name=name)
            state.save()
            return HttpResponseRedirect("/order/state")
    else:
        state_data=Order_State.objects.all()
        if request.GET.get('id'):
            state_form=Order_StateForm(model_to_dict(Order_State.objects.get(pk=request.GET.get('id'))))
        else:
            state_form=Order_StateForm()
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
            quantity=data['quantity']
            delivery=data['delivery_bill']
            product=data['product']
            stock=data['stock']
            stock_product=Stock_Product(quantity=quantity,delivery=delivery,product=product,stock=stock)
            stock_product.save()
            return HttpResponseRedirect("/order/stock_product")
    else:
        stock_product_data=Stock_Product.objects.all()
        if request.GET.get('id'):
            stock_product_form=Stock_ProductForm(model_to_dict(Stock_Product.objects.get(pk=request.GET.get('id'))))
        else:
            stock_product_form=Stock_ProductForm()
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
def order_product(request):
    if request.method=="POST":
        product_form=ProductForm(request.POST)
        if product_form.is_valid():
            data=product_form.cleaned_data
            name=data['name']
            price=data['price']
            delivery_type=data['delivery_type']
            stock=data['stock']
            product=Product(name=name,price=price,delivery_type=delivery_type,stock=stock)
            product.save()
            return HttpResponseRedirect("/order/product")
    else:
        product_data=Product.objects.all()
        if request.GET.get('id'):
            product_form=ProductForm(model_to_dict(Product.objects.get(pk=request.GET.get('id'))))
        else:
            product_form=ProductForm()
        stock_form=StockForm()
        form_list={
               'product_data':product_data,
               'product_form':product_form,
               'stock_form':stock_form
               }
        return render(request,'order_product.html',form_list)
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
            name=data['name']
            person=Issuing_person(name=name)
            person.save()
            return HttpResponseRedirect("/order/issuing_person")
    else:
        issuing_person_data=Issuing_person.objects.all()
        if request.GET.get('id'):
            issuing_person_form=Issuing_personForm(model_to_dict(Issuing_person.objects.get(pk=request.GET.get('id'))))
        else:
            issuing_person_form=Issuing_personForm()
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