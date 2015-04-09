#coding=utf-8
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.contrib.auth.views import login_required
from forms import *
from django.contrib.auth.models import User,Group,Permission,ContentType
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.forms import UserCreationForm
from stock.models import *
from role.models import *
from order.models import *
import json


@login_required(login_url="/login")
def home(request):
    #if request.user.is_superuser:

    return render(request,'home.html')
def permission_deny(request):
    return HttpResponse("<script language='javascript'>alert('没有权限');history.go(-1)</script>")
def login_validate(request,username,password):
    rtvalue = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth_login(request,user)
            return True
    return rtvalue
def mylogin(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request,username,password):
                return HttpResponseRedirect('/home')
            else:
                error.append('密码错误')
        else:
            error.append('输入有错误')
    else:
        form = LoginForm()
    return render(request,'login.html',{'error':error,'form':form})
@login_required(login_url='/login')
def mylogout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login')
@login_required(login_url='/login')
def changepassword(request,username):
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=username,password=data['old_pwd'])
            if user is not None:
                if data['new_pwd']==data['new_pwd2']:
                    newuser = User.objects.get(username__exact=username)
                    newuser.set_password(data['new_pwd'])
                    newuser.save()
                    response=HttpResponse()
                    response.write("<script language='javascript'>alert('修改成功!');window.location.href='/login/';</script>")
                    return response
                else:
                    error.append('请输入相同的密码')
            else:
                error.append('请输入正确的旧密码')
        else:
            error.append('请按照规则输入')
    else:
        form = ChangepwdForm()
    return render(request,'change_password.html',{'form':form,'error':error})

def admin_required(login_url=None):
    return user_passes_test(lambda u:u.is_superuser,login_url=login_url)

@admin_required(login_url='/login')
def user_info(request):
    user=User.objects.all()
    user_form=UserForm()
    return render(request,'user_info.html',{'userinfo':user,'user_form':user_form})

@admin_required(login_url="/login")
def user_add(request):
    if request.method=='POST':
        response=HttpResponse()
        user_form=UserForm(request.POST)
        #print user_form
        if user_form.is_valid():
            data=user_form.cleaned_data
            #print data
            #print request.POST
            user=user_form.save(commit=False)
            user.username=data["username"]
            user.first_name=data["first_name"]
            user.email=data["email"]
            user.set_password(data["password"])
            user.save()
            groups=[request.POST.get("group")]
            user.groups=groups
            response.write("<script language='javascript'>alert('添加成功!');window.location.href='/user/info/';</script>")
            return response
        else:
            response.write("<script language='javascript'>alert('添加失败!');window.location.href='/user/info/';</script>")
            return response
    # else:
    #     return render(request,'add_role.html',{'userform':form,'role':role})

@admin_required(login_url='/login')
def user_remove(request):
    user_id=request.GET.get("id")
    response=HttpResponse()
    user=User.objects.get(pk=user_id)
    if user.is_superuser:
        response.write("<script language='javascript'>alert('管理员无法删除!');window.location.href='/user/info/';</script>")
    else:
        user.delete()
        response.write("<script language='javascript'>alert('删除成功!');window.location.href='/user/info/';</script>")
    return response

@admin_required(login_url='/login')
def user_edit(request):
    if request.method=="POST":
        #print request.POST
        name=request.POST.get('name')
        if name=='password':
            user=User.objects.get(pk=request.POST.get("pk"))
            value=request.POST.get('value')
            user.set_password(value)
            user.save()
            return HttpResponse('success')
        else:
            value=request.POST.get('value')
            info_dict={'%s'%name:value}
            user=User.objects.filter(pk=request.POST.get("pk"))
            user.update(**info_dict)
        return HttpResponse('success')

@admin_required(login_url='/login')
def user_group_edit(request,username):
    if request.method=='POST':
        group_form=UsergroupForm(request.POST)
        response=HttpResponse()
        if group_form.is_valid():
            data=group_form.cleaned_data
            groups=[request.POST.get('groups')]
            user=User.objects.get(username=username)
            user.groups=groups
            user.save()
            response.write("<script language='javascript'>alert('修改成功!');window.location.href=('/user/info/')</script>")
            return response
        else:
            response.write("<script language='javascript'>alert('修改失败!请联系管理员');window.history.go(-1)</script>")
            return response

    else:
        group_form=UsergroupForm(instance=User.objects.get(username=username))
        #group_form.fields['groups'].initail=User.objects.get(username=username).groups.last()
    return render(request,'user_group_edit.html',{'group_form':group_form,'username':username})

# @admin_required(login_url='/login')
# def user_permission_edit(request,username):
#     if request.method=='POST':
#         permission_form=UserpermissionForm(request.POST)
#         if permission_form.is_valid():
#             data=permission_form.cleaned_data
#     else:
#         permission_form=UserpermissionForm(instance=User.objects.get(username=username))
#     return render(request,'user_permission_edit.html',{'permission_form':permission_form})

@admin_required(login_url='/login')
def role_info(request):
    group=Group.objects.all()
    group_form=GroupForm()
    data_json=get_all_permissions()
    return render(request,'role_info.html',{'group':group,'group_form':group_form,'data_json':data_json})



@admin_required(login_url="/login")
def role_name_add(request):
    if request.method=='POST':
        response=HttpResponse()
        role_form=GroupForm(request.POST)
        #print request.POST
        if role_form.is_valid():
            role=role_form.save(commit=False)
            role.name=request.POST.get('name')
            role.save()
            permissions=request.POST.get("authchecked")
            if permissions:
                permission_array=permissions.split(',')
                permission_list=[int(i) for i in permission_array if i.isdigit()]
                role.permissions=permission_list
                role.save()
            #role_form.save_m2m()
        #role_name.save()
            response.write("<script language='javascript'>alert('添加成功!');window.location.href=('/role/info')</script>")
            return response
        else:
            response.write("<script language='javascript'>alert('添加失败!');window.location.href=('/role/info')</script>")
            return response
    # return render(request,'add_role.html',{'role':role})
@admin_required(login_url="/login")
def role_name_edit(request,role_id):
    if request.method=='POST':
        response=HttpResponse()
        role_form=GroupForm(request.POST)
        name=request.POST.get('name')
        if name:
            role=Group.objects.get(pk=role_id)
            role.name=name
            permissions=request.POST.getlist('permissions')
            role.permissions=permissions
            role.save()
            response.write("<script language='javascript'>alert('修改成功!');window.location.href=('/role/info/')</script>")
            return response
        else:
            response.write("<script language='javascript'>alert('修改失败!名称不能为空');window.history.go(-1)</script>")
            return response
    else:
        role_form=GroupForm(instance=Group.objects.get(pk=role_id))
    #print role_form
        #role_form.fields['permissions'].initial=Group.objects.get(pk=id).permissions.all()
    return render(request,'role_name_edit.html',{'group_form':role_form})
@admin_required(login_url='/login')
def role_name_remove(request):
    role_name_id=request.GET.get('id')
    response=HttpResponse()
    role_object=Group.objects.get(pk=role_name_id)
    # links=[rel.get_accessor_name() for rel in role_object._meta.get_all_related_objects()]
    # for link in links:
    #     objects=getattr(role_object,link).all()
    #     for object in objects:
    #         object.user.delete()
    #         object.delete()
    # role_object.delete()
    role_object.delete()
    response.write("<script language='javascript'>alert('删除成功!');window.location.href='/role/info/';</script>")
    return response

def get_all_permissions():
    permission_choices=[u'原料',u'产品',u'客户水平',u'客户',u'订单状态',u'联系方式',u'订单',u'出单人',u'角色',u'客户导入',u'订单导入']
    data_json={'text':u'权限','children':[]}
    for i in permission_choices:
        if i ==u'原料':
            permission=Permission.objects.filter(content_type=ContentType.objects.get(name=i))
            for k in permission:
                if 'Can change' in k.name:
                    data_dict={'id':str(k.id),'text':u'仓管(填写单号)'}
            data_json['children'].append(data_dict)
        else:
            data_dict={'text':i,'children':[]}
            permission=Permission.objects.filter(content_type=ContentType.objects.get(name=i))
            for k in permission:
                if 'Can add' in k.name:
                    data_dict['children'].append({'id':str(k.id),'text':k.name.replace('Can add ',u'添加')})
                elif 'Can change' in k.name:
                    data_dict['children'].append({'id':str(k.id),'text':k.name.replace('Can change ',u'修改')})
                else:
                    data_dict['children'].append({'id':str(k.id),'text':k.name.replace('Can delete ',u'删除')})
            data_json['children'].append(data_dict)
            data_dict={}
    data_json=json.dumps(data_json)
    #return HttpResponse(str(data_json))
    return data_json