# coding=utf-8
# from django.contrib.auth.models import User,Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
# from django.db.models import Q
# import json
# from models import *
from forms import *
from django.forms.formsets import formset_factory
# from django.utils.translation import gettext as _
from role.models import *
import math
import json


def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


@admin_required(login_url='/login/')
def user_log_info(request):
    if request.method == "POST":
        username = request.POST.get('user')
        filter_dict = {}
        initial = {}
        if username:
            user_log = UserLog.objects.filter(
                user=User.objects.get(pk=username))
            initial['user'] = User.objects.get(pk=username)
        else:
            user_log = UserLog.objects.all()
        model_type = request.POST.get('type')
        if model_type:
            user_log = user_log.filter(model_name=model_type)
            filter_dict['type'] = model_type
        starttime = request.POST.get('starttime')
        if starttime:
            user_log = user_log.filter(jointime__gte=starttime)
            filter_dict['starttime'] = starttime
        endtime = request.POST.get('endtime')
        if endtime:
            user_log = user_log.filter(jointime__lte=endtime)
            filter_dict['endtime'] = endtime
        page = request.POST.get('page')
        if page:
            # total_page = int(math.ceil(float(len(user_log)) / 20))
            if int(page) == 1:
                start_page = 0
                end_page = 20
            else:
                start_page = 20 * (int(page) - 1)
                end_page = 20 * int(page)
            user_log = user_log[start_page:end_page]
            return render(request, 'user_log_pagination.html',
                          {'user_log': user_log})

        else:
            # start_page = 0
            end_page = 20
            total_page = int(math.ceil(float(len(user_log)) / 20))
            user_log = user_log[:end_page]
            page = 1

    else:
        filter_dict = {}
        total_page = 0
        page = 0
        user_log = []
        initial = {}
    if initial:
        log_form = User_LogForm(initial=initial)
    else:
        log_form = User_LogForm()
    return render(request, 'user_log_info.html', {
        'form': log_form,
        'filter': filter_dict,
        'user_log': user_log,
        'total_page': total_page,
        'current_page': page
    })


@admin_required(login_url='/login')
def get_object_info(request):
    log_id = request.GET.get('id')
    # object_id=int(request.GET.get('object_id'))
    # #print object_type,object_id
    # if object_type == "Order":
    #     try:
    #         object_model=Order.objects.get(pk=object_id)
    #     except:
    #         return HttpResponse('该订单已被删除')
    # else:
    #     try:
    #         object_model=Customer.objects.get(pk=object_id)
    #     except:
    #         return HttpResponse("该客户已被删除")
    user_log = UserLog.objects.get(pk=log_id)
    data = json.loads(user_log.data['data'])
    return render(request, 'get_object_info.html',
                  {'data': data,
                   'object': user_log})


@admin_required(login_url="/login")
def customer_custom_design(request):
    table_design_formset = formset_factory(Table_designForm,
                                           max_num=10,
                                           validate_max=True,
                                           min_num=0,
                                           extra=1)
    if request.method == "POST":
        # total_forms = request.POST.get('form-TOTAL_FORMS')
        post_dict = dict(request.POST.iteritems())
        # print post_dict,type(post_dict)
        formset = table_design_formset(post_dict, prefix='customer')
        # print formset.is_valid()
        table_list = []
        column_id = 1
        for form in formset:
            if form.is_valid():
                data = form.cleaned_data
                try:
                    name = data['name']
                except KeyError:
                    return HttpResponse("字段名称不能为空", status=400)
                if name:
                    data['column_id'] = column_id
                    column_id += 1
                    # print data
                    table_list.append(data)
                else:
                    continue
        table_dict = {'data': json.dumps(table_list)}
        customer_table = Table_Design(schema_model='customer',
                                      schema_data=table_dict)
        customer_table.save()
        return HttpResponseRedirect(redirect_to='/customer/column/setting/')
    else:
        customer_table = Table_Design.objects.filter(
            schema_model='customer').order_by('-jointime')
        if customer_table:
            data = json.loads(customer_table[0].schema_data['data'])
            formset = table_design_formset(prefix='customer', initial=data)
        else:
            formset = table_design_formset(prefix='customer')
    return render(request, 'customer_custom.html', {'formset': formset})