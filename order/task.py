# coding=utf-8
from __future__ import absolute_import

from celery import task
from order.models import *
from django.contrib.auth.models import User
from notifications import notify


@task
def alert(alert_user, request_user, alert_content, alert_time, phone, customer):
    alert_user = User.objects.get(username=alert_user)
    request_user = User.objects.get(username=request_user)
    notify.send(request_user, recipient=alert_user, verb=alert_content, description='%s:%s' % (customer, phone))
    # print alert_user,request_user,alert_content,alert_time
    customer_alert = Customer_Alert.objects.filter(alert_user=User.objects.get(
        username=alert_user),add_user=request_user, content=alert_content, alert_time=alert_time)
    customer_alert.update(alert_state=True)
    print 'success'
