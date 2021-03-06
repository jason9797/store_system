# coding=utf-8
import urllib
import ast

from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from role.forms import *
from forms import *
from order import task
import math
from store_system.celery import app
import json
from datetime import datetime, timedelta


@permission_required('order.add_order', login_url='/permission/deny/')
def order_add(request):
    """
    添加订单
    """
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
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
            # delivery_no=data['delivery_no']
            # fact_money=data['fact_money']
            customer = data['customer']
            issuing_person = data['issuing_person']
            product = data['product']
            remark = data['remark']
            # order_state=data['state']
            order = Order(delivery_no='',
                          fact_money=0,
                          customer=customer,
                          issuing_person=issuing_person,
                          product=product,
                          state=Order_State.objects.get(name='未发货'),
                          remark=remark)

            order.save()
            data = {}
            for i in order._meta.fields:
                try:
                    verbose_name = order._meta.get_field(
                        i.name).verbose_name.title().decode('utf-8')
                except:
                    verbose_name = order._meta.get_field(
                        i.name).verbose_name.title()
                # print verbose_name
                # print inspect.isclass(type(getattr(order,i.name))),getattr(order,i.name),type(getattr(order,i.name)),dir(getattr(order,i.name))
                if hasattr(getattr(order, i.name), '_meta'):
                    data[verbose_name] = getattr(order, i.name).__unicode__()
                else:
                    if isinstance(getattr(order, i.name), datetime):
                        data[verbose_name] = (
                            getattr(order, i.name) + timedelta(hours=8)
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        data[verbose_name] = getattr(order, i.name)
            data = json.dumps(data)
            data = {'data': data}
            UserLog.objects.create(
                user=request.user,
                action='create',
                model_name=order.__class__.__name__,
                model_object_id=order.id,
                data=data)
            if request.user.is_superuser:
                js_data = "<script language='javascript'>var r=confirm('添加成功,确定继续添加,取消返回到订单列表!');\
                if (r==true){  window.location.href='/order/order/add/?customer_id=%s'}else\
                {window.location.href='/order/order/'}</script>" % customer.id
            else:
                js_data = "<script language='javascript'>var r=confirm('添加成功,确定继续添加,取消返回到订单列表!');\
                if (r==true){  window.location.href='/order/order/add/?customer_id=%s'}else\
                {window.location.href='/order/my_order/'}</script>" % customer.id
            return HttpResponse(js_data)
        # else:
        #    print order_form.errors
    else:
        # if request.GET.get('id'):
        #     order_form=OrderForm(model_to_dict(Order.objects.get(pk=request.GET.get('id'))))
        # else:
        if request.GET.get('customer_id'):
            customer = Customer.objects.get(pk=request.GET.get("customer_id"))
            order_form = OrderForm({'customer': customer})
        else:
            order_form = OrderForm()

    # order_data=Order.objects.all()
    # customer_form=CustomerForm()
    # issuing_person_form=Issuing_personForm()
    # product_form=ProductForm()
    # order_state_form=Order_StateForm()
    form_list = {
        # 'order_data':order_data,
        'order_form': order_form,
        # 'customer_form':customer_form,
        # 'issuing_person_form':issuing_person_form,
        # 'product_form':product_form,
        # 'order_state_form':order_state_form,
    }
    return render(request, 'order_add.html', form_list)


@permission_required('order.change_order', login_url='/permission/deny')
def order_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        value = request.POST.get('value')
        if name == 'customer':
            value = Customer.objects.get(name=value)
        if name == "issuing_person":
            value = Issuing_person.objects.get(name=value)
        if name == 'product':
            value = Product.objects.get(name=value)
        if name == 'state':
            value = Order_State.objects.get(name=value)
            cur_order_state = Order.objects.get(pk=request.POST.get("pk")).state
            if not request.user.is_superuser:
                if value.level < cur_order_state.level:
                    # raise Http404
                    return HttpResponse("修改失败,必须按顺序操作", status=404)
            if cur_order_state.level == 1 and value.level > 1:
                return HttpResponse("请联系仓管或管理员填写订单号,自动修改状态", status=400)
            # print value
        info_dict = {'%s' % name: value}
        order = Order.objects.filter(pk=request.POST.get("pk"))
        data = {}
        try:
            verbose_name = order[0]._meta.get_field(name).verbose_name.title(
            ).decode('utf-8')
        except:
            verbose_name = order[0]._meta.get_field(name).verbose_name.title()
        # print verbose_name
        # print inspect.isclass(type(getattr(order,i.name))),getattr(order,i.name),type(getattr(order,i.name)),dir(getattr(order,i.name))
        if hasattr(getattr(order[0], name), '_meta'):
            data[verbose_name] = [getattr(order[0], name).__unicode__(),
                                  value.__unicode__()]
        else:
            data[verbose_name] = [getattr(order[0], name), value]
        data = json.dumps(data)
        data = {'data': data}
        UserLog.objects.create(
            user=request.user,
            action='edit',
            model_name=order[0].__class__.__name__,
            model_object_id=order[0].id,
            data=data)
        order.update(**info_dict)
        if name == 'delivery_no':
            product = Order.objects.get(pk=request.POST.get('pk')).product
            # stock_product=Stock_Product.objects.filter(product=product)
            stock_management = Stock_Management(
                stock_mode=True,
                product=product,
                mode=Stock_Mode.objects.get(pk=1))
            stock_management.save()
        # user_log=UserLog(user=request.user,action='edit',model_name=order[0].__class__.__name__,model_object_id=order[0].id)
        # user_log.save()
        return HttpResponse('success')


@permission_required('order.delete_order', login_url='/permission/deny')
def order_home_remove(request):
    order_id = request.GET.get("id")
    order = Order.objects.get(pk=order_id)
    # print order.state
    if order.state != Order_State.objects.get(level=1):
        return HttpResponse(
            "<script language='javascript'>alert('订单已发货或结束，无法删除!');window.history.go(-1);</script>",
            status=400)
    else:
        # user_log=UserLog(user=request.user,action='delete',model_name=order.__class__.__name__,model_object_id=order_id)
        # user_log.save()
        data = {}
        for i in order._meta.fields:
            try:
                verbose_name = order._meta.get_field(
                    i.name).verbose_name.title().decode('utf-8')
            except:
                verbose_name = order._meta.get_field(
                    i.name).verbose_name.title()
            # print verbose_name
            # print inspect.isclass(type(getattr(order,i.name))),getattr(order,i.name),type(getattr(order,i.name)),dir(getattr(order,i.name))
            if hasattr(getattr(order, i.name), '_meta'):
                data[verbose_name] = getattr(order, i.name).__unicode__()
            else:
                if isinstance(getattr(order, i.name), datetime):
                    data[verbose_name] = (getattr(order, i.name) + timedelta(
                        hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data[verbose_name] = getattr(order, i.name)
        data = json.dumps(data)
        data = {'data': data}
        UserLog.objects.create(user=request.user, action='delete', model_name=order.__class__.__name__,
                               model_object_id=order.id, data=data)
        order.delete()
    return HttpResponse(
        "<script language='javascript'>alert('删除成功!');window.location.href=document.referrer;</script>")


@permission_required('order.add_customer', login_url='/permission/deny')
def order_customer_add(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            data = customer_form.cleaned_data
            name = data['name']
            sex = data['sex']
            level = data['level']
            # issuing_person=data['issuing_person']
            if request.user.is_superuser:
                user = None
            else:
                user = request.user
            # print request.POST
            customer_table = Table_Design.objects.filter(
                schema_model="customer").order_by('-jointime')[0]
            customer_extra = json.loads(customer_table.schema_data['data'])
            customer_dict = {}
            for i in customer_extra:
                if i['required'] == True:
                    customer_dict[i['name']] = request.POST.get('%s' % i['column_id'])
            # print customer_dict
            customer = Customer(name=name,
                                sex=sex,
                                level=level,
                                user=user,
                                data=customer_dict)
            customer.save()
            province = request.POST.get('province')
            city = request.POST.get('city')
            country = request.POST.get('country')
            street = request.POST.get('street')
            address = province + city + country + street + data['address']
            phone_number = data['phone_number']
            contact = Contact_info(address=address,
                                   phone_number=phone_number,
                                   customer=customer,
                                   default=True)
            contact.save()
            # user_log=UserLog(user=request.user,action='create',model_name=customer.__class__.__name__,model_object_id=customer.id)
            # user_log.save()

            data = {u'地址': address, u'手机号码': phone_number}
            for i in customer._meta.fields:
                try:
                    verbose_name = customer._meta.get_field(
                        i.name).verbose_name.title().decode('utf-8')
                except:
                    verbose_name = customer._meta.get_field(
                        i.name).verbose_name.title()
                # print verbose_name
                # print inspect.isclass(type(getattr(customer,i.name))),getattr(customer,i.name),type(getattr(customer,i.name)),dir(getattr(customer,i.name))
                if hasattr(getattr(customer, i.name), '_meta'):
                    data[verbose_name] = getattr(customer, i.name).__unicode__()
                else:
                    if isinstance(getattr(customer, i.name), datetime):
                        data[verbose_name] = (
                            getattr(customer, i.name) + timedelta(hours=8)
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        data[verbose_name] = getattr(customer, i.name)

            data = json.dumps(data)
            data = {'data': data}
            UserLog.objects.create(
                user=request.user,
                action='create',
                model_name=customer.__class__.__name__,
                model_object_id=customer.id,
                data=data)
            js_data = "<script language='javascript'>var r=confirm('添加成功,确定继续添加,取消返回到客户列表!');if (r==true){  window.location.href='/order/customer/add'}else{window.location.href='/order/customer/'}</script>"
            return HttpResponse(js_data)

    else:
        # if request.GET.get("id"):
        #    customer_form=CustomerForm(model_to_dict(Customer.objects.get(pk=request.GET.get("id"))))
        # else:
        default_data = {'level': Customer_Level.objects.get(level = 1)}
        customer_form = CustomerForm(default_data)
    # customer_data=Customer.objects.all()
    level_form = Customer_LevelForm()
    try:
        customer_extra = json.loads(
            Table_Design.objects.filter(schema_model='customer').order_by(
                '-jointime')[0].schema_data['data'])
    except:
        customer_extra = []
    form_list = {
        # 'customer_data':customer_data,
        'customer_form': customer_form,
        'customer_level': level_form,
        'customer_extra': customer_extra,
        # 'table_widget':table_widget
    }
    return render(request, 'order_customer_add.html', form_list)


@permission_required('order.delete_customer', login_url='/permission/deny')
def order_customer_remove(request):
    if request.GET.get("id_list"):
        id_list = [int(i) for i in request.GET.get("id_list").split(',')
                   if i.isdigit()]
        for i in Customer.objects.filter(id__in=id_list):
            customer_delete_log(i, request.user)
        Customer.objects.filter(id__in=id_list).delete()
        return HttpResponse('success', status=200)
    customer_id = request.GET.get("id")
    customer = Customer.objects.get(pk=customer_id)
    customer_delete_log(customer, request.user)
    customer.delete()
    # user_log=UserLog(user=request.user,action='delete',model_name=customer.__class__.__name__,model_object_id=customer_id)
    # user_log.save()
    return HttpResponseRedirect("/order/customer")


def customer_delete_log(customer, request_user):
    address = customer.get_contact_info()[0].address
    phone_number = customer.get_contact_info()[0].phone_number
    data = {u'地址': address, u'手机号码': phone_number}
    for i in customer._meta.fields:
        try:
            verbose_name = customer._meta.get_field(
                i.name).verbose_name.title().decode('utf-8')
        except:
            verbose_name = customer._meta.get_field(i.name).verbose_name.title()
        # print verbose_name
        # print inspect.isclass(type(getattr(customer,i.name))),getattr(customer,i.name),type(getattr(customer,i.name)),dir(getattr(customer,i.name))
        if hasattr(getattr(customer, i.name), '_meta'):
            data[verbose_name] = getattr(customer, i.name).__unicode__()
        else:
            if isinstance(getattr(customer, i.name), datetime):
                data[verbose_name] = (getattr(customer, i.name) + timedelta(
                    hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[verbose_name] = getattr(customer, i.name)

    data = json.dumps(data)
    data = {'data': data}
    UserLog.objects.create(user=request_user, action='delete', model_name=customer.__class__.__name__,
                           model_object_id=customer.id, data=data)


@permission_required('order.change_customer', login_url='/permission/deny')
def customer_other(request):
    return render(request, 'customer_other.html')


@permission_required('order.change_customer_level',
                     login_url='/permission/deny')
def order_customer_level(request):
    # if request.method=="POST":
    #     customer_level_form=Customer_LevelForm(request.POST)
    #     if customer_level_form.is_valid():
    #         data=customer_level_form.cleaned_data
    #         if request.GET.get("id"):
    #             customer_level=Customer_Level.objects.get(pk=request.GET.get('id'))
    #             customer_level.level=data['level']
    #             customer_level.save()
    #         return HttpResponseRedirect("/order/customer_level")
    # else:
    #     if request.GET.get("id"):
    #         customer_level_form=Customer_LevelForm(model_to_dict(Customer_Level.objects.get(pk=request.GET.get("id"))))
    #     else:
    #         customer_level_form=Customer_LevelForm()
    customer_level_form = Customer_LevelForm()
    customer_level_data = Customer_Level.objects.all()
    form_list = {
        'customer_level_data': customer_level_data,
        'customer_level_form': customer_level_form,
    }
    return render(request, 'order_customer_level.html', form_list)


@permission_required('order.add_customer_level', login_url='/permission/deny')
def order_customer_level_add(request):
    if request.method == "POST":
        customer_level_form = Customer_LevelForm(request.POST)
        if customer_level_form.is_valid():
            data = customer_level_form.cleaned_data
            level = data['level']
            name = data['name']
            customer_level = Customer_Level(level=level, name=name)
            customer_level.save()
            return HttpResponseRedirect("/order/customer_level")
    else:
        customer_level_form = Customer_LevelForm()
        print dir(customer_level_form.errors)
    return render(request, 'order_customer_level_add.html',
                  {'form': customer_level_form})


@permission_required('order.change_customer_level',
                     login_url='/permission/deny')
def order_customer_level_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        value = request.POST.get('value')
        info_dict = {'%s' % name: value}
        customer_level = Customer_Level.objects.filter(
            pk=request.POST.get("pk"))
        customer_level1 = Customer_Level.objects.filter(level=1)
        if len(customer_level1) == 1:
            return HttpResponse("只能存留一个基本等级", status=400)
        customer_level.update(**info_dict)
        return HttpResponse('success')


@permission_required('order.delete_customer_level',
                     login_url='/permission/deny')
def order_customer_level_remove(request):
    level_id = request.GET.get("id")
    level = Customer_Level.objects.get(pk=level_id)
    if level.level == 1:
        level_list = Customer_Level.objects.filter(level=1)
        if len(level_list) == 1:
            return HttpResponse(
                "<script language='javascript'>alert('等级为1不能删除');window.location.href=document.referrer;</script>")
        else:
            level.delete()
    else:
        level.delete()
    return HttpResponseRedirect("/order/customer_level")


@permission_required('order.add_contact_info', login_url='/permission/deny')
def order_contact_add(request):
    if request.method == "POST":
        contact_form = Contact_infoForm(request.POST)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            # if request.GET.get("id"):
            #     contact=Contact_info.objects.get(pk=request.GET.get('id'))
            #     contact.address=data['address']
            #     contact.phone_number=data['phone_number']
            #     contact.customer=data['customer']
            #     contact.save()
            # else:
            province = request.POST.get('province')
            city = request.POST.get('city')
            country = request.POST.get('country')
            street = request.POST.get('street')
            address = province + city + country + street + data['address']
            phone_number = data['phone_number']
            customer = data['customer']
            default = request.POST.get('default')
            if default:
                Contact_info.objects.filter(customer=customer).update(
                    default=False)
                contact = Contact_info(address=address,
                                       phone_number=phone_number,
                                       customer=customer,
                                       default=default)
            else:
                contact = Contact_info(address=address,
                                       phone_number=phone_number,
                                       customer=customer)
            contact.save()
            return HttpResponseRedirect("/order/contact/add")
    else:
        if request.GET.get('id'):
            contact_form = Contact_infoForm(
                initial=
                {'customer': Customer.objects.get(pk = request.GET.get('id'))})
        else:
            contact_form = Contact_infoForm()
    # contact_data=Contact_info.objects.all()
    # customer_form=CustomerForm()
    form_list = {
        # 'contact_data':contact_data,
        # 'customer_form':customer_form,
        'contact_form': contact_form
    }
    return render(request, 'order_contact_add.html', form_list)


@permission_required('order.delete_contact_info', login_url='/permission/deny')
def order_contact_remove(request):
    contact_id = request.GET.get("id")
    contact = Contact_info.objects.get(pk=contact_id)
    contact.delete()
    return HttpResponseRedirect("/order/contact")


@permission_required('order.change_contact_info', login_url='/permission/deny')
def order_contact_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        try:
            value = eval(request.POST.get('value[]'))
        except:
            value = request.POST.get('value')

        if name == 'customer':
            value = Customer.objects.get(name=value)
        info_dict = {'%s' % name: value}
        contact = Contact_info.objects.filter(pk=request.POST.get("pk"))
        contact.update(**info_dict)
        return HttpResponse('success')
    if request.GET.get("customer_id"):
        customer_id = request.GET.get("customer_id")
        contact_id = request.GET.get("contact_id")
        Contact_info.objects.filter(
            customer=Customer.objects.get(pk=customer_id)).update(default=False)
        contact_info = Contact_info.objects.get(pk=contact_id)
        contact_info.default = True
        contact_info.save()
        return HttpResponseRedirect("/order/customer")


@permission_required('order.change_contact_info', login_url='/permission/deny')
def order_contact(request):
    if request.method == 'POST':
        # province=request.POST.get('province')
        # city=request.POST.get('city')
        # country=request.POST.get('country')
        # street=request.POST.get('street')
        # address=province+city+country+street
        address = request.POST.get('address')
        filter_dict = {}
        initial = {}
        if address:
            contact = Contact_info.objects.filter(address__contains=address)
            filter_dict['address'] = address
        else:
            contact = Contact_info.objects.all()
        default = request.POST.get('default')
        if default:
            contact = contact.filter(default=eval(default))
            filter_dict['default'] = eval(default)
        phone_number = request.POST.get('phone_number')
        if phone_number:
            # contact=contact.filter(phone_number__contains=phone_number)
            contact = contact.filter(phone_number=phone_number)
            filter_dict['phone_number'] = phone_number
        customer = request.POST.get('Customer')
        if customer:
            contact = contact.filter(
                customer=Customer.objects.get(pk=int(customer)))
            initial['customer'] = Customer.objects.get(pk=int(customer))
        form = Contact_infoForm(initial)
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(contact)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            contact = contact[start_page:end_page]
            customer = Customer.objects.all()
            return render(request, 'contact_pagination.html',
                          {'contact': contact,
                           'customer': customer})

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(contact)) / 20))
            contact = contact[:end_page]
            page = 1
    else:
        form = Contact_infoForm()
        contact = []
        filter_dict = {}
        total_page = 0
        page = 0
    customer = Customer.objects.all()
    info = {
        'form': form,
        'contact': contact,
        'filter': filter_dict,
        'customer': customer,
        'total_page': total_page,
        'current_page': page
    }
    return render(request, 'order_contact.html', info)


@permission_required('order.add_order_state', login_url='/permission/deny')
def order_state(request):
    if request.method == "POST":
        state_form = Order_StateForm(request.POST)
        if state_form.is_valid():
            data = state_form.cleaned_data
            name = data['name']
            state = Order_State(name=name, level=3)
            state.save()
            return HttpResponse(
                "<script language='javascript'>alert('添加成功');window.location.href=document.referrer;</script>")
    else:
        state_form = Order_StateForm()
    state_data = Order_State.objects.all()
    form_list = {'state_data': state_data, 'state_form': state_form}
    return render(request, 'order_state.html', form_list)


@permission_required('order.change_order_state', login_url='/permission/deny')
def order_state_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        value = request.POST.get('value')
        info_dict = {'%s' % name: value}
        order_state = Order_State.objects.filter(pk=int(request.POST.get("pk")))
        order_state.update(**info_dict)
        return HttpResponse("success")


@permission_required('order.delete_order_state', login_url='/permission/deny')
def order_state_remove(request):
    state_id = request.GET.get("id")
    state = Order_State.objects.get(pk=state_id)
    if state.level < 3:
        return HttpResponse(
            "<script language='javascript'>alert('无法删除默认订单状态');window.location.href=document.referrer;</script>")
    state.delete()
    return HttpResponseRedirect("/order/state")


@permission_required('order.add_stock_product', login_url='/permission/deny')
def order_stock_product_add(request):
    if request.method == "POST":
        stock_product_form = Stock_ProductForm(request.POST)
        if stock_product_form.is_valid():
            data = stock_product_form.cleaned_data
            # if request.GET.get("id"):
            #     stock_product=Stock_Product.objects.get(pk=request.GET.get('id'))
            #     stock_product.quantity-=data['quantity']
            #     stock_product.delivery_bill=data['delivery_bill']
            #     stock_product.product=data['product']
            #     stock_product.stock=data['stock']
            #     stock_product.save()
            # else:
            quantity = data['quantity']
            delivery = data['delivery_bill']
            product = data['product']
            stock = data['stock']
            stock_product = Stock_Product(quantity=quantity,
                                          delivery_bill=delivery,
                                          product=product,
                                          stock=stock)
            stock_product.save()
            return HttpResponseRedirect("/order/stock_product")
    else:
        # if request.GET.get('id'):
        #     stock_product_form=Stock_ProductForm(model_to_dict(Stock_Product.objects.get(pk=request.GET.get('id'))))
        # else:
        stock_product_form = Stock_ProductForm()
    # stock_product_data=Stock_Product.objects.all()
    form_list = {
        # 'stock_product_data':stock_product_data,
        'stock_product_form': stock_product_form,  #'stock_form':StockForm
    }
    return render(request, 'order_stock_product_add.html', form_list)


@permission_required('order.change_stock_product', login_url='/permission/deny')
def order_stock_product_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        try:
            value = eval(request.POST.get('value[]'))
        except:
            value = request.POST.get('value')
        # print value
        if name == 'stock':
            value = Stock.objects.get(name=value)
        if name == 'product':
            value = Product.objects.get(name=value)
        info_dict = {'%s' % name: value}
        stock_product = Stock_Product.objects.filter(pk=request.POST.get("pk"))
        stock_product.update(**info_dict)
        return HttpResponse('success')


@permission_required('order.delete_stock_product', login_url='/permission/deny')
def order_stock_product_remove(request):
    stock_product_id = request.GET.get("id")
    stock_product = Stock_Product.objects.get(pk=stock_product_id)
    stock_product.delete()
    return HttpResponseRedirect("/order/stock_product")


@permission_required('order.change_stock_product', login_url='/permission/deny')
def order_stock_product(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        filter_dict = {}
        initial = {}
        if quantity:
            stock_product = Stock_Product.objects.filter(
                quantity__contains=quantity)
            filter_dict['quantity'] = quantity
        else:
            stock_product = Stock_Product.objects.all()
        delivery_bill = request.POST.get('delivery_bill')
        if delivery_bill:
            stock_product = stock_product.filter(
                delivery_bill=eval(delivery_bill))
            filter_dict['delivery_bill'] = eval(delivery_bill)
        product = request.POST.get('product')
        # print stock_product
        if product:
            stock_product = stock_product.filter(
                product=Product.objects.get(pk=int(product)))
            initial['product'] = Product.objects.get(pk=int(product))
        stock = request.POST.get('stock')
        if stock:
            stock_product = stock_product.filter(
                stock=Stock.objects.get(pk=int(stock)))
            initial['stock'] = Stock.objects.get(pk=int(stock))
        form = Stock_ProductForm(initial)
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(stock_product)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            stock_product = stock_product[start_page:end_page]
            product = Product.objects.all()
            stock = Stock.objects.all()
            return render(request, 'stock_product_pagination.html', {
                'stock_product': stock_product,
                'product': product,
                'stock': stock
            })

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(stock_product)) / 20))
            stock_product = stock_product[:end_page]
            page = 1
    else:
        form = Stock_ProductForm()
        stock_product = []
        filter_dict = {}
        total_page = 0
        page = 0
    product = Product.objects.all()
    stock = Stock.objects.all()
    info = {
        'form': form,
        'stock_product': stock_product,
        'filter': filter_dict,
        'stock': stock,
        'product': product,
        'total_page': total_page,
        'current_page': page
    }
    return render(request, 'order_stock_product.html', info)


@permission_required('order.add_product', login_url='/permission/deny')
def order_product_add(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            data = product_form.cleaned_data
            name = data['name']
            price = data['price']
            delivery_type = data['delivery_type']
            detail = data['detail']
            product = Product(name=name,
                              price=price,
                              delivery_type=delivery_type,
                              detail=detail)
            product.save()
            js_data = "<script language='javascript'>var r=confirm('添加成功,确定继续添加,取消返回到产品列表!');\
            if (r==true){  window.location.href='/order/product/add/'}else" \
                      "{window.location.href='/order/product/'}</script>"
            return HttpResponse(js_data)
            # return HttpResponseRedirect("/order/product")
    else:
        product_form = ProductForm()
    form_list = {'product_form': product_form,}
    return render(request, 'order_product_add.html', form_list)


@permission_required('order.change_product', login_url='/permission/deny')
def order_product_edit(request):
    if request.method == "POST":
        print request.POST
        name = request.POST.get('name')
        if name == 'price':
            value = float(request.POST.get('value'))
        else:
            value = request.POST.get('value')
        info_dict = {'%s' % name: value}
        product = Product.objects.filter(pk=request.POST.get("pk"))
        product.update(**info_dict)
        return HttpResponse('success')


@permission_required('order.delete_product', login_url='/permission/deny')
def order_product_remove(request):
    product_id = request.GET.get("id")
    product = Product.objects.get(pk=product_id)
    product.delete()
    return HttpResponseRedirect("/order/product")


@permission_required('order.add_issuing_person', login_url='/permission/deny')
def order_issuing_person(request):
    if request.method == "POST":
        issuing_person_form = Issuing_personForm(request.POST)
        if issuing_person_form.is_valid():
            data = issuing_person_form.cleaned_data
            name = data['name']
            person = Issuing_person(name=name)
            person.save()
            return HttpResponse(
                "<script language='javascript'>alert('添加成功');window.location.href=document.referrer;</script>")
    else:
        issuing_person_form = Issuing_personForm()
    issuing_person_data = Issuing_person.objects.all()
    form_list = {
        'issuing_person_data': issuing_person_data,
        'issuing_person_form': issuing_person_form
    }
    return render(request, 'order_issuing_person.html', form_list)


@permission_required("order.change_issuing_person",
                     login_url='/permission/deny')
def order_issuing_person_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        value = request.POST.get('value')
        info_dict = {'%s' % name: value}
        issuing_person = Issuing_person.objects.filter(
            pk=int(request.POST.get("pk")))
        issuing_person.update(**info_dict)
        return HttpResponse("success")


@permission_required('order.delete_issuing_person',
                     login_url='/permission/deny')
def order_issuing_person_remove(request):
    person_id = request.GET.get("id")
    person = Issuing_person.objects.get(pk=person_id)
    person.delete()
    return HttpResponseRedirect("/order/issuing_person")


@permission_required('order.change_customer', login_url='/permission/deny')
def my_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        filter_dict = {}
        initial = {}
        if name:
            customer = Customer.objects.filter(name__contains=name)
            filter_dict['name'] = name
        else:
            customer = Customer.objects.all()
        level = request.POST.get('level')
        if level:
            customer = customer.filter(
                level=Customer_Level.objects.get(pk=level))
            initial['level'] = Customer_Level.objects.get(pk=level)
        sex = request.POST.get('sex')
        if sex:
            customer = customer.filter(sex=eval(sex))
            filter_dict['sex'] = eval(sex)
        server = request.POST.get('user')
        # print server
        # print customer
        if request.user.is_superuser:
            if server:
                customer = customer.filter(
                    user=User.objects.get(pk=int(server)))
                initial['user'] = User.objects.get(pk=int(server))
            # else:
            #     customer=customer.filter(user__in=User.objects.filter(is_superuser=False))
            # customer=customer.filter(user__in=UserProfile.objects.filter(role=Role.objects.get(name=u'客服')).values('user'))
            # initial['user']=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        else:
            customer = customer.filter(user=request.user)
            initial['user'] = request.user

        issuing_person = request.POST.get('issuing_person')
        if issuing_person:
            try:
                customer = customer.filter(
                    issuing_person=
                    Issuing_person.objects.get(pk=int(issuing_person)))
                initial['issuing_person'] = Issuing_person.objects.get(
                    pk=int(issuing_person))
            except:
                return HttpResponseRedirect('/order/my_customer')

        starttime = request.POST.get('starttime')
        if starttime:
            customer = customer.filter(jointime__gte=starttime)
            filter_dict['starttime'] = starttime
        endtime = request.POST.get('endtime')
        if endtime:
            customer = customer.filter(jointime__lte=endtime)
            filter_dict['endtime'] = endtime
        form = CustomerForm(initial)
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(customer)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            # print start_page,end_page
            # total_page=math.ceil(float(len(customer))/20)
            # customer_json=serializers.serialize('json',customer[start_page:end_page])
            # print customer_json
            customer = customer[start_page:end_page]
            # return HttpResponse(customer.query)
            level = Customer_Level.objects.all()
            if request.user.is_superuser:
                userlist = User.objects.all(pk__in=UserProfile.objects.filter(role=u'客服').values('id'))
            else:
                userlist = User.objects.filter(pk=request.user.id)
            issuing_person = Issuing_person.objects.all()
            return render(request, 'my_customer_pagination.html', {
                'customer': customer,
                'userlist': userlist,
                'level': level,
                'issuing_person': issuing_person
            })

        else:
            # print customer
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(customer)) / 20))
            customer = customer[:end_page]
            # return HttpResponse(customer.query)
            # print total_page
            page = 1
        # print customer
        # customer=Customer.objects.filter(name__contains=name,level=Customer_Level.objects.get(pk=level),
        #      sex=sex,user=User.objects.get(pk=server),issuing_person=Issuing_person.objects.get(pk=issuing_person),
        #  jointime__gte=starttime,jointime__lte=endtime)
    else:
        form = CustomerForm()
        if request.user.is_superuser:
            server = UserProfile.objects.filter(
                role=Role.objects.get(name=u'客服'))
        else:
            server = UserProfile.objects.filter(user=request.user)
        if request.user.is_superuser:
            form.fields['user'].queryset = UserProfile.objects.filter(
                role=Role.objects.get(name=u'客服'))
        else:
            form.fields['user'].queryset = UserProfile.objects.filter(
                user=request.user)
        customer = []
        filter_dict = {}
        total_page = 0
        page = 0
    level = Customer_Level.objects.all()
    if request.user.is_superuser:
        userlist = User.objects.filter(id__in=UserProfile.objects.filter(
            role=Role.objects.get(name=u'客服')).values('user'))
    else:
        userlist = User.objects.filter(pk=request.user.id)
    issuing_person = Issuing_person.objects.all()
    info = {
        "server": server,
        'form': form,
        'customer': customer,
        'filter': filter_dict,
        'total_page': total_page,
        'current_page': page,
        'level': level,
        'issuing_person': issuing_person,
        'userlist': userlist
    }
    return render(request, 'my_customer.html', info)


@permission_required('order.change_customer', login_url='/permission/deny')
def order_customer_edit(request):
    if request.method == "POST":
        # print request.POST
        name = request.POST.get('name')
        if name == 'address' or name == 'phone_number':
            value = request.POST.get('value')
            contact = Contact_info.objects.filter(
                customer=Customer.objects.get(pk=request.POST.get("pk")))
            if True in contact.values_list('default'):
                contact = contact.filter(default=True)
            contact.update(**{'%s' % name: value})
            return HttpResponse('success')
        try:
            value = eval(request.POST.get('value[]'))
        except:
            value = request.POST.get('value')
        if name == 'user':
            value = User.objects.get(username=value)
        if name == "level":
            try:
                value = Customer_Level.objects.get(name=value)
            except:
                value = Customer_Level.objects.filter(name=value)[0]
        if not value:
            raise Http404
        info_dict = {'%s' % name: value}
        # print info_dict
        customer = Customer.objects.filter(pk=request.POST.get("pk"))
        customer_edit_log(customer[0], request.user, name, value)
        customer.update(**info_dict)
        # user_log=UserLog(user=request.user,action='edit',model_name=customer[0].__class__.__name__,model_object_id=customer[0].id)
        # user_log.save()
        return HttpResponse('success')
    else:
        if request.GET.get("id_list"):
            id_list = [int(i) for i in request.GET.get("id_list").split(',')
                       if i.isdigit()]
            server = request.GET.get('server')
            for i in Customer.objects.filter(id__in=id_list):
                customer_edit_log(i, request.user, 'user',
                                  User.objects.get(username=server))
            Customer.objects.filter(id__in=id_list).update(**{'user': User.objects.get(username = server)})
            return HttpResponse('success', status=200)
        # customer_id = request.GET.get('customer_id')
        if request.user.is_superuser:
            pass
        else:
            customer = Customer.objects.get(pk=request.GET.get("customer_id"))
            customer_edit_log(customer, request.user, 'user', request.user)
            customer.user = request.user
            customer.save()
            return HttpResponse(
                "<script language='javascript'>alert('归属成功');window.location.href=document.referrer;</script>")


def customer_edit_log(customer, request_user, name, value):
    data = {}
    try:
        verbose_name = customer._meta.get_field(name).verbose_name.title(
        ).decode('utf-8')
    except:
        verbose_name = customer._meta.get_field(name).verbose_name.title()
    # print verbose_name
    # print inspect.isclass(type(getattr(customer,i.name))),getattr(customer,i.name),type(getattr(customer,i.name)),dir(getattr(customer,i.name))
    if hasattr(getattr(customer, name), '_meta'):
        data[verbose_name] = [getattr(customer, name).__unicode__(),
                              value.__unicode__()]
    else:
        if hasattr(value, '_meta'):
            data[verbose_name] = [getattr(customer, name), value.__unicode__()]
        else:
            data[verbose_name] = [getattr(customer, name), value]
    data = json.dumps(data)
    data = {'data': data}
    UserLog.objects.create(user=request_user,action='edit',
                           model_name=customer.__class__.__name__, model_object_id=customer.id, data=data)


@permission_required('order.change_customer', login_url='/permission/deny')
def order_customer(request):
    if request.method == 'POST':
        filter_dict = {}
        initial = {}
        # address=request.POST.get('address[]')
        address = request.POST.get('address')
        if address:
            filter_dict['address'] = address
            customer = Customer.objects.filter(
                pk__in=Contact_info.objects.filter(
                    Q(address__contains=
                      address) & Q(default=True)).values_list('customer'))
        else:
            customer = Customer.objects.all()
        # phone_number=request.POST.get("phone_number[]")
        phone_number = request.POST.get("phone_number")
        if phone_number:
            filter_dict['phone_number'] = phone_number
            customer = customer.filter(pk__in=Contact_info.objects.filter(
                phone_number=phone_number).values_list('customer'))

        # print customer.query.__str__()
        name = request.POST.get('name')
        if name:
            customer = customer.filter(name__contains=name)
            filter_dict['name'] = name
        level = request.POST.get('level')
        if level:
            customer = customer.filter(
                level=Customer_Level.objects.get(pk=level))
            initial['level'] = Customer_Level.objects.get(pk=level)
        sex = request.POST.get('sex')
        if sex:
            customer = customer.filter(sex=eval(sex))
            filter_dict['sex'] = eval(sex)
        user_null = request.POST.get("usernull")
        # print user_null
        server = request.POST.get('user')
        if user_null:
            customer = customer.filter(user__isnull=True)
            initial['usernull'] = True
            filter_dict['usernull'] = True
            # print customer.query.__str__()
        else:
            if request.user.is_superuser:
                if server:
                    customer = customer.filter(
                        user=User.objects.get(pk=int(server)))
                    initial['user'] = User.objects.get(pk=int(server))
                else:
                    customer = customer.filter(user__isnull=False)
                    initial['usernull'] = False
                    filter_dict['usernull'] = False
                # else:
                #     customer=customer.filter(user__in=User.objects.filter(is_superuser=False))
                # customer=customer.filter(user__in=UserProfile.objects.filter(role=Role.objects.get(name=u'客服')).values('user'))
                # initial['user']=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
            else:
                customer = customer.filter(
                    Q(user=request.user) & Q(user__isnull=False))
                initial['user'] = request.user
        # issuing_person=request.POST.get('issuing_person')
        # if issuing_person:
        #     try:
        #         customer=customer.filter(issuing_person=Issuing_person.objects.get(pk=int(issuing_person)))
        #         initial['issuing_person']=Issuing_person.objects.get(pk=int(issuing_person))
        #     except:
        #         return HttpResponseRedirect('/order/customer')

        starttime = request.POST.get('starttime')
        if starttime:
            filter_dict['starttime'] = starttime
            filter_dict['starthour'] = request.POST.get("start_hour")
            filter_dict['startminute'] = request.POST.get("start_minute")
            starttime = starttime + ' %s:%s:00' % (request.POST.get("start_hour"), request.POST.get("start_minute"))
            # print starttime
            customer = customer.filter(jointime__gte=starttime)
            # filter_dict['starttime']=starttime
        endtime = request.POST.get('endtime')
        if endtime:
            filter_dict['endtime'] = endtime
            filter_dict['endhour'] = request.POST.get("end_hour")
            filter_dict['endminute'] = request.POST.get("end_minute")
            endtime = endtime + ' %s:%s:00' % (request.POST.get("end_hour"), request.POST.get("end_minute"))
            customer = customer.filter(jointime__lte=endtime)
            # filter_dict['endtime']=endtime
        form = CustomerForm(initial)
        page = request.POST.get('page')
        if page:
            # print len(customer)
            # total_page = int(math.ceil(float(len(customer)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            customer = customer.order_by('-jointime')[start_page:end_page]
            level = Customer_Level.objects.all()
            # print customer.query.__str__()
            return render(request, 'customer_pagination.html',
                          {'customer': customer,
                           'level': level})

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(customer)) / 20))
            customer = customer.order_by('-jointime')[:end_page]
            page = 1
    else:
        form = CustomerForm()
        # server=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        server = User.objects.filter(is_superuser=False)
        form.fields['user'].queryset = User.objects.filter(is_superuser=False)
        # form.fields['user'].queryset=UserProfile.objects.filter(role=Role.objects.get(name=u'客服'))
        customer = []

        filter_dict = {}
        total_page = 0
        page = 0
    user_list = User.objects.all()
    hour_list = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
    minute_list = ["0" + str(i) if i < 10 else str(i) for i in range(0, 60, 5)]
    level = Customer_Level.objects.all()
    info = {
        "server": server,
        'form': form,
        'customer': customer,
        'level': level,
        'filter': filter_dict,
        'total_page': total_page,
        'current_page': page,
        "hour_list": hour_list,
        "minute_list": minute_list,
        'user_list': user_list
    }
    return render(request, 'order_customer.html', info)


# @permission_required(login_url='/permission/deny')
@permission_required('order.change_product', login_url='/permission/deny')
def order_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        filter_dict = {}
        initial = {}
        if name:
            product = Product.objects.filter(name__contains=name)
            filter_dict['name'] = name
        else:
            product = Product.objects.all()
        starttime = request.POST.get('starttime')
        if starttime:
            product = product.filter(jointime__gte=starttime)
            filter_dict['starttime'] = starttime
        endtime = request.POST.get('endtime')
        if endtime:
            product = product.filter(jointime__lte=endtime)
            filter_dict['endtime'] = endtime
        form = ProductForm(initial)
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(product)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            product = product[start_page:end_page]
            return render(request, 'product_pagination.html',
                          {'product': product})

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(product)) / 20))
            product = product[:end_page]
            page = 1
    else:
        form = ProductForm()
        product = []
        filter_dict = {}
        total_page = 0
        page = 0
    info = {
        'form': form,
        'product': product,
        'filter': filter_dict,
        'total_page': total_page,
        'current_page': page
    }
    return render(request, 'order_product.html', info)


@permission_required('order.change_order', login_url='/permission/deny')
def order_info(request):
    if request.method == 'POST':
        filter_dict = {}
        initial = {}
        address = request.POST.get('address')
        if address:
            order = Order.objects.filter(customer__in=Customer.objects.filter(
                pk__in=Contact_info.objects.filter(
                    Q(address__contains=
                      address) & Q(default=True)).values_list('customer')))
            filter_dict['address'] = address
        else:
            order = Order.objects.all()
        phone_number = request.POST.get("phone_number")
        if phone_number:
            order = order.filter(customer__in=Customer.objects.filter(
                pk__in=Contact_info.objects.filter(
                    Q(phone_number=
                      phone_number) & Q(default=True)).values_list('customer')))
            filter_dict['phone_number'] = phone_number
        delivery_no = request.POST.get('delivery_no')
        if delivery_no:
            order = order.filter(delivery_no=delivery_no)
            filter_dict['delivery_no'] = delivery_no
        # else:
        # order=Order.objects.all()
        fact_money = request.POST.get('fact_money')
        if fact_money:
            order = order.filter(fact_money=fact_money)
            filter_dict['fact_money'] = fact_money
        customer = request.POST.get('customer[]')
        if customer:
            order = order.filter(
                customer=Customer.objects.filter(name=customer))
            # initial['customer']=Customer.objects.get(pk=int(customer))
            filter_dict['customer'] = customer

        issuing_person = request.POST.get('issuing_person[]')
        if issuing_person:
            try:
                order = order.filter(issuing_person=Issuing_person.objects.get(
                    name=issuing_person))
                # initial['issuing_person']=Issuing_person.objects.get(pk=int(issuing_person))
                filter_dict['issuing_person'] = issuing_person
            except:
                return HttpResponseRedirect('/order/order/info')
        product = request.POST.get('product[]')
        if product:
            try:
                order = order.filter(
                    product=Product.objects.filter(name=product))
                filter_dict['product'] = product
                # initial['product']=Product.objects.get(pk=int(product))
            except:
                return HttpResponseRedirect('/order/order/info')

        state = request.POST.get('state')
        if state:
            try:
                order = order.filter(
                    state=Order_State.objects.get(pk=int(state)))
                initial['state'] = Order_State.objects.get(pk=int(state))
            except:
                return HttpResponseRedirect('/order/order/info')

        starttime = request.POST.get('starttime')
        if starttime:
            filter_dict['starttime'] = starttime
            filter_dict['starthour'] = request.POST.get("start_hour")
            filter_dict['startminute'] = request.POST.get("start_minute")
            starttime = starttime + ' %s:%s:00' % (request.POST.get("start_hour"), request.POST.get("start_minute"))
            order = order.filter(jointime__gte=starttime)
            # filter_dict['starttime']=starttime
        endtime = request.POST.get('endtime')
        if endtime:
            filter_dict['endtime'] = endtime
            filter_dict['endhour'] = request.POST.get("end_hour")
            filter_dict['endminute'] = request.POST.get("end_minute")
            endtime = endtime + ' %s:%s:00' % (request.POST.get("end_hour"), request.POST.get("end_minute"))
            order = order.filter(jointime__lte=endtime)
            # filter_dict['endtime']=endtime
        form = OrderForm(initial)
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(order)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            order = order.order_by('-jointime')[start_page:end_page]
            state_list = Order_State.objects.all()
            product_list = Product.objects.all()
            customer_list = Customer.objects.all()
            issuing_person_list = Issuing_person.objects.all()
            return render(request, 'order_pagination.html', {
                'order': order,
                'state': state_list,
                'product': product_list,
                'customer': customer_list,
                'issuing_person': issuing_person_list
            })

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(order)) / 20))
            order = order.order_by('-jointime')[:end_page]
            page = 1
    else:
        form = OrderForm()
        filter_dict = {}
        total_page = 0
        page = 0
        order = []
    state_list = Order_State.objects.all()
    product_list = Product.objects.all()
    customer_list = Customer.objects.all()
    issuing_person_list = Issuing_person.objects.all()
    hour_list = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
    minute_list = ["0" + str(i) if i < 10 else str(i) for i in range(0, 60, 5)]
    info = {
        'form': form,
        'filter': filter_dict,
        'order': order,
        'total_page': total_page,
        'current_page': page,
        'state': state_list,
        'product': product_list,
        'customer': customer_list,
        'issuing_person': issuing_person_list,
        "hour_list": hour_list,
        "minute_list": minute_list
    }
    return render(request, 'order_info.html', info)


@permission_required('order.change_contact_info', login_url='/permission/deny')
def get_position(request):
    customer_id = request.GET.get('customer')
    contact = Contact_info.objects.filter(
        customer=Customer.objects.get(pk=customer_id))
    return render(request, 'get_position.html', {'contact': contact})


@login_required(login_url="/login")
def order_other(request):
    return render(request, 'order_other.html')


@login_required(login_url="/login")
def order_trace(request):
    delivery_no = request.GET.get('delivery_no')
    try:

        order_type = get_order_info(delivery_no)[0]
        trace_info = get_order_trace_info(delivery_no, order_type)
        # print trace_info
        return render(request, 'order_trace.html', {'trace': trace_info})
    except:
        return HttpResponse("没有订单信息，请查看订单号是否正确")


def get_order_info(num):

    order = urllib.urlopen("http://www.kuaidi100.com/autonumber/auto?num=%s" % num)
    order_info = eval(order.read())
    order_type = [i['comCode'] for i in order_info]
    # print order_type
    return order_type


def get_order_trace_info(num, Type):

    order = urllib.urlopen("http://www.kuaidi100.com/query?type=%s&postid=%s" %
                           (Type, num))
    order_info = order.read()
    info = ast.literal_eval(order_info)['data']
    # [0]['context'].decode('utf-8')
    info = sorted(info, key=lambda k: k['time'], reverse=False)
    return info


@login_required(login_url="/login")
def my_order_info(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse(
            "<script language='javascript'>alert('请用客服账号查看');window.location.href=document.referrer;</script>")
    order_info = Order.objects.filter(Q(
        customer__in=Customer.objects.filter(user=user)) & Q(state__in=Order_State.objects.filter(
        Q(name=_("已发货未签收")) | Q(name=_("未发货"))))).order_by("-jointime")
    state_list = Order_State.objects.all()

    return render(request, "my_order.html",
                  {"order": order_info,
                   'state': state_list})


@login_required(login_url="/login")
def get_customer_info(request):
    customer_id = request.GET.get("customer_id")
    customer = Customer.objects.get(pk=customer_id)
    contact_info = Contact_info.objects.filter(customer=customer)
    order_info = Order.objects.filter(customer=customer).order_by("-jointime")
    try:
        server_record = Order_Server.objects.filter(order=order_info[0])
    except:
        server_record = []
    # print server_record
    return render(request, 'get_customer_info.html', {
        "customer": customer,
        "contact_info": contact_info,
        "order_info": order_info,
        'server_record': server_record
    })


@login_required(login_url="/login")
def order_server_record(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        customer = Customer.objects.get(pk=customer_id)
        order = customer.get_recent_order()[0]
        if order:
            content = request.POST.get("content")
            order_server = Order_Server(order=order, content=content)
            order_server.save()
            return HttpResponse(
                "<script language='javascript'>alert('设置备注成功');window.location.href=document.referrer;</script>")
        else:
            return HttpResponse(
                "<script language='javascript'>alert('设置失败');</script>")


@login_required(login_url="/login")
def customer_alert_add(request):
    if request.method == "POST":
        customer = request.POST.get("customer")
        phone_number = request.POST.get("phone_number")
        alert_time = request.POST.get("date") + ' %s:%s:00' % (
            request.POST.get("hour"), request.POST.get("minute"))
        alert_user = User.objects.get(username=request.POST.get("alert_user"))
        alert_content = request.POST.get("alert_content")
        add_user = request.user.username
        customer_alert = Customer_Alert(customer=customer,
                                        content=alert_content,
                                        phone_number=phone_number,
                                        alert_time=alert_time,
                                        alert_user=alert_user,
                                        add_user=add_user)
        customer_alert.save()
        alert_time = datetime.datetime.strptime(alert_time, "%Y-%m-%d %H:%M:%S")
        do_time = alert_time - datetime.timedelta(hours=8)
        # 传到celery多了8个小时

        # print do_time
        task_result = task.alert.apply_async(
            (request.POST.get("alert_user"), request.user.username,
             alert_content, alert_time, phone_number, customer),
            eta=do_time)
        task_id = task_result.id
        customer_alert.task_id = task_id
        customer_alert.save()
        # app.control.revoke(task_id,terminate=True)
        return HttpResponse(
            "<script language='javascript'>alert('添加提醒成功');window.location.href=document.referrer;</script>")
    else:
        customer_id = request.GET.get('customer_id')
        customer = Customer.objects.get(pk=int(customer_id))
        user_list = User.objects.all()
        hour_list = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
        minute_list = ["0" + str(i) if i < 10 else str(i)
                       for i in range(0, 60, 5)]
        return render(request, 'customer_alert_add.html', {
            'customer': customer,
            'user_list': user_list,
            'hour_list': hour_list,
            'minute_list': minute_list
        })


@login_required(login_url='/login')
def customer_alert_info(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        filter_dict = {}
        if customer:
            customer_alert = Customer_Alert.objects.filter(
                customer__contains=customer)
            filter_dict['customer'] = customer
        else:
            customer_alert = Customer_Alert.objects.all()
        alert_state = request.POST.get('alert_state')
        if alert_state == 'All' or not alert_state:
            filter_dict['alert_state'] = 'All'
        else:
            customer_alert = customer_alert.filter(
                alert_state=eval(alert_state))
            filter_dict['alert_state'] = eval(alert_state)
        alert_user = request.POST.get('alert_user')
        if alert_user:
            # contact=contact.filter(phone_number__contains=phone_number)
            customer_alert = customer_alert.filter(
                alert_user=User.objects.get(username=alert_user))
            filter_dict['alert_user'] = alert_user
        starttime = request.POST.get('starttime')
        if starttime:
            customer_alert = customer_alert.filter(jointime__gte=starttime)
            filter_dict['starttime'] = starttime
        endtime = request.POST.get('endtime')
        if endtime:
            customer_alert = customer_alert.filter(jointime__lte=endtime)
            filter_dict['endtime'] = endtime
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(customer_alert)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            customer_alert = customer_alert[start_page:end_page]
            user_list = User.objects.all()
            return render(
                request, 'alert_pagination.html',
                {'customer_alert': customer_alert,
                 'user_list': user_list})

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(customer_alert)) / 20))
            customer_alert = customer_alert[:end_page]
            page = 1
    else:
        customer_alert = []
        filter_dict = {}
        total_page = 0
        page = 0
    user_list = User.objects.all()
    info = {
        'customer_alert': customer_alert,
        'filter': filter_dict,
        'user_list': user_list,
        'total_page': total_page,
        'current_page': page
    }
    return render(request, 'customer_alert.html', info)


@login_required(login_url='/login')
def customer_alert_remove(request):
    customer_alert_id = request.GET.get("id")
    customer_alert = Customer_Alert.objects.get(pk=customer_alert_id)
    if customer_alert.alert_state:
        customer_alert.delete()
    else:
        app.control.revoke(customer_alert.task_id, terminate=True)
        customer_alert.delete()
    return HttpResponse("<script language='javascript'>alert('删除成功');</script>")