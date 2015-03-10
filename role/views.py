#coding=utf-8
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.contrib.auth.views import login_required
from forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
login_required(login_url="/login/")
def home(request):
    return render(request,'home.html')
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

@login_required(login_url='/login')
def role_info(request):
    if request.method=='POST':
        response=HttpResponse()
        username=request.POST.get("username")
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        user=User.objects.get(username__exact=username)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        if len(password1)==0 and len(password2)==0:
            user.save()
            response.write("<script language='javascript'>alert('信息修改完成!');window.location.href='/role';</script>")
        elif password1!=password2:
            response.write("<script language='javascript'>alert('两次密码不一致!');window.location.href='/role';</script>")
        else:
            if len(password1)<6:
                response.write("<script language='javascript'>alert('密码长度必须大于等于6位!');window.location.href='/role';</script>")
            else:
                user.set_password(password1)
                user.save()
                response.write("<script language='javascript'>alert('信息修改完成!');window.location.href='/login';</script>")
        return response
    if request.user.is_superuser:
        role_info=UserProfile.objects.all()
    else:
        role_info=UserProfile.objects.get(user=request.user)
    form=UserCreationForm()
    return render(request,'role.html',{'role':role_info,'form':form})
def admin_required(login_url=None):
    return user_passes_test(lambda u:u.is_superuser,login_url=login_url)

@admin_required(login_url='/login')
def add_role(request,role):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username=data['username']
            if role=='0':
                role=False
            else:
                role=True
            response=HttpResponse()
            roleuser=UserProfile(user=User.objects.get(username=username),role=role)
            roleuser.save()
            response.write("<script language='javascript'>alert('添加成功!');window.location.href='/role';</script>")
            return response
        else:
            response=HttpResponse()
            response.write("<script language='javascript'>alert('表单信息错误!');window.location.href='/role';</script>")
            return response
    else:
        return render(request,'add_role.html',{'userform':form,'role':role})

