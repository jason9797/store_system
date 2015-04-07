__author__ = 'jason_lee'
#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.translation import gettext as _
import csv
import xlrd
from models import *
from forms import *
from store_system import settings





@permission_required('order.add_customerfile',login_url='/permission/deny')
def customer_file(request):
    if request.method=='POST':
        form=CustomerFileForm(request.POST,request.FILES)
        #print request.FILES
        if form.is_valid():
            # for filename,file in request.FILES.iteritems():
            #     #print file,filename
            #     name=request.FILES[filename].name
            customerfile=CustomerFile(file=request.FILES['file'],title=request.POST.get('title'))
            customerfile.save()
            file_type=customerfile.file.name.split('.')[-1]
            filename=settings.MEDIA_ROOT+'/'+customerfile.file.name
            if file_type=='txt':
                f=open(filename,'rb')
                data=f.readlines()
                for i in data:
                    info=i.split()
                    name=info[0]
                    sex=True if info[1]=='男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=info[2]
                    phone_number=info[3]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
                f.close()
            if file_type=='csv':
                csvfile=file(filename,'rb')
                reader=csv.reader(csvfile)
                for line in reader:
                    name=line[0]
                    sex=True if line[1]=='男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=info[2]
                    phone_number=info[3]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
                csvfile.close()
            if file_type in ['xls','xlsx']:
                excel=xlrd.open_workbook(filename)
                data=excel.sheets()[0]
                nrows=data.nrows
                for i in range(nrows):
                    name=data.cell(i,0).value
                    sex=True if data.cell(i,1).value==u'男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=data.cell(i,2).value
                    phone_number=str(data.cell(i,3).value).split('.')[0]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
            return HttpResponse("<script language='javascript'>alert('上传成功');history.go(-1)</script>")
        else:
            return HttpResponse("<script language='javascript'>alert('未知错误');history.go(-1)</script>")
    else:
        form=CustomerFileForm()
    return render(request,"customer_upload.html",{'form':form})


@permission_required('order.add_orderfile',login_url='/permission/deny')
def order_file(request):
    if request.method=='POST':
        form=OrderFileForm(request.POST,request.FILES)
        #print request.FILES
        if form.is_valid():
            # for filename,file in request.FILES.iteritems():
            #     #print file,filename
            #     name=request.FILES[filename].name
            orderfile=OrderFile(file=request.FILES['file'],title=request.POST.get('title'))
            orderfile.save()
            file_type=orderfile.file.name.split('.')[-1]
            filename=settings.MEDIA_ROOT+'/'+orderfile.file.name
            if file_type=='txt':
                f=open(filename,'rb')
                data=f.readlines()
                for i in data:
                    info=i.split()
                    name=info[0]
                    sex=True if info[1]=='男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=info[2]
                    phone_number=info[3]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
                    try:
                        issuing_person=Issuing_person.objects.get(name=_(info[4]))
                    except:
                        issuing_person=None
                    try:
                        product=Product.objects.get(name=_(info[5]))
                    except:
                        product=None
                    order=Order(customer=customer,issuing_person=issuing_person,product=product,
                                state=Order_State.objects.get(name=_("未发货")))
                    order.save()
                f.close()
            if file_type=='csv':
                csvfile=file(filename,'rb')
                reader=csv.reader(csvfile)
                for line in reader:
                    name=line[0]
                    sex=True if line[1]=='男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=info[2]
                    phone_number=info[3]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
                    try:
                        issuing_person=Issuing_person.objects.get(name=_(info[4]))
                    except:
                        issuing_person=None
                    try:
                        product=Product.objects.get(name=_(info[5]))
                    except:
                        product=None
                    order=Order(customer=customer,issuing_person=issuing_person,product=product,
                                state=Order_State.objects.get(name=_("未发货")))
                    order.save()
                csvfile.close()
            if file_type in ['xls','xlsx']:
                excel=xlrd.open_workbook(filename)
                data=excel.sheets()[0]
                nrows=data.nrows
                for i in range(nrows):
                    name=data.cell(i,0).value
                    sex=True if data.cell(i,1).value==u'男' else False
                    level=Customer_Level.objects.get(level=1)
                    customer=Customer(name=name,sex=sex,level=level)
                    customer.save()
                    address=data.cell(i,2).value
                    phone_number=str(data.cell(i,3).value).split('.')[0]
                    contact=Contact_info(address=address,phone_number=phone_number,customer=customer,default=True)
                    contact.save()
                    try:
                        issuing_person=Issuing_person.objects.get(name=_(data.cell(i,4).value))
                    except:
                        issuing_person=None
                    try:
                        product=Product.objects.get(name=_(data.cell(i,5).value))
                    except:
                        product=None
                    order=Order(customer=customer,issuing_person=issuing_person,product=product,
                                state=Order_State.objects.get(name=_("未发货")))
                    order.save()
            return HttpResponse("<script language='javascript'>alert('上传成功');history.go(-1)</script>")
        else:
            return HttpResponse("<script language='javascript'>alert('未知错误');history.go(-1)</script>")
    else:
        form=OrderFileForm()
    return render(request,"order_upload.html",{'form':form})