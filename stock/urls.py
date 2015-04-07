#__author__ = 'jason_lee'
from django.conf.urls import *
from views import *
urlpatterns=patterns('',
            url(r'^add/$',stock_add,name='stock_add'),
            url(r'^remove/$',stock_remove,name='stock_remove'),
            url(r'^edit/$',stock_edit,name="stock_edit"),
            url(r'^info/$',stock_info,name='stock_info'),
            url(r'^other/$',stock_other,name="stock_other"),
            url(r'^type/$',stock_type,name='stock_type'),
            url(r'^type/remove/$',stock_type_remove,name='stock_type_remove'),
            url(r'^channel/$',stock_channel,name='stock_channel'),
            url(r'^channel/remove/$',stock_channel_remove,name='stock_channel_remove'),
            url(r'^management/$',stock_management,name="stock_management"),
            url(r'^management/edit$',stock_management_edit,name="stock_management_edit"),
            url(r'^management/remove/$',stock_management_remove,name="stock_management_remove"),
            url(r'^mode/$',stock_mode,name="stock_mode"),
            url(r'^mode/remove/$',stock_mode_remove,name="stock_mode_remove"),
            url(r'^order/no/$',stock_order_no,name="stock_order_no"),
        #url(r'^role/edit/(?P<id>\d+)$',edit_role,name="edit_role"),
        #url(r'^role/remove$',remove_role,name="remove_role"),
)