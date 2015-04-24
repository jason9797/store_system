#coding=utf-8
from order.models import *
from django.utils.translation import gettext as _
customer_level=Customer_Level(name=_('普通用户'),level=1)
customer_level.save()
state=[('未发货',1),('已发货未签收',2),('已签收',3),('丢失',3),('快递转移',3)]
for i in state:
    order_state=Order_State.objects.get(name=_(i[0]),level=i[1])
    order_state.save()
