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
import datetime
import json
from models import *
from forms import *

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    ##
    
