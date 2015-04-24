from django.conf.urls import *
from views import *
from report_views import *
from contact_views import *
from file_upload import *
urlpatterns=patterns('',
            url(r'^order/other/$',order_other,name='order_other'),
            url(r'^order/add/$',order_add,name='order_add'),
            url(r'^order/$',order_info,name='order_info'),
            url(r'^order/edit$',order_edit,name='order_edit'),
            url(r'^order/remove$',order_home_remove,name='order_remove'),
            url(r'^customer/$',order_customer,name="order_customer"),
            url(r'^customer/add$',order_customer_add,name='order_customer_add'),
            url(r'^customer/edit/$',order_customer_edit,name='order_customer_edit'),
            url(r'^customer/remove/$',order_customer_remove,name='order_customer_remove'),
            url(r'^my_customer/$',my_customer,name="my_customer"),
            url(r'^customer/other/$',customer_other,name='customer_other'),
            url(r'^customer_level/add/$',order_customer_level_add,name='order_customer_level_add'),
            url(r'^customer_level/edit/$',order_customer_level_edit,name='order_customer_level_edit'),
            url(r'^customer_level/$',order_customer_level,name='order_customer_level'),
            url(r'^customer_level/remove/$',order_customer_level_remove,name='order_customer_level_remove'),
            url(r'^contact/add/$',order_contact_add,name="order_contact_add"),
            url(r'^contact/edit/$',order_contact_edit,name="order_contact_edit"),
            url(r'^contact/$',order_contact,name='order_contact'),
            url(r'^contact/remove/$',order_contact_remove,name='order_contact_remove'),
            url(r'^get/position/$',get_position,name='get_position'),
            url(r'^state/$',order_state,name='order_state'),
            url(r'^state/edit/$',order_state_edit,name='order_state_edit'),
            url(r'^state/remove/$',order_state_remove,name='order_state_remove'),
            url(r'^stock_product/add$',order_stock_product_add,name='order_stock_product_add'),
            url(r'^stock_product/$',order_stock_product,name='order_stock_product'),
             url(r'^stock_product/edit/$',order_stock_product_edit,name='order_stock_product_edit'),
            url(r'^stock_product/remove/$',order_stock_product_remove,name='order_stock_product_remove'),
            url(r'^product/add/$',order_product_add,name='order_product_add'),
            url(r'^product/$',order_product,name='order_product'),
            url(r'^product/edit/$',order_product_edit,name='order_product_edit'),
            url(r'^product/remove/$',order_product_remove,name='order_product_remove'),
            url(r'^issuing_person/$',order_issuing_person,name='order_issuing_person'),
            url(r'^issuing_person/edit/$',order_issuing_person_edit,name='order_issuing_person_edit'),
            url(r'^issuing_person/remove/$',order_issuing_person_remove,name='order_issuing_person_remove'),
            url(r'^customer/upload/$',customer_file,name='customer_upload'),
            url(r'^order/upload/$',order_file,name='order_upload'),
            url(r'^income/reporter/$',income_reporter,name='income_reporter'),
            url(r'^issuing/reporter/$',issuing_person_reporter,name='issuing_person_reporter'),
            url(r'^get/contact/address/$',get_contact_address,name="get_contact_address"),
            url(r'^get/contact/phone/$',get_contact_phone,name="get_contact_phone"),
            url(r'^get/all/product/$',get_all_product,name="get_all_product"),
            url(r'^get/all/customer/$',get_all_customer,name="get_all_customer"),
            url(r'^get/all/issuing_person/$',get_all_issuing_person,name="get_all_issuing_person"),
            url(r'^order/trace/$',order_trace,name="get_order_trace"),
            url(r'^my_order/$',my_order_info,name="my_order_info"),
            url(r'^get/customer/info/$',get_customer_info,name="get_customer_info"),
            url(r'^person/sale/report/$',person_sale_report,name="person_sale_report"),
            url(r'^team/sale/report/$',team_sale_report,name="team_sale_report"),
            url(r'^success/report/$',order_success_report,name="order_success_report"),
            url(r'^alert/sign_order/$',alert_message,name="alert_sign_order"),
            url(r'^alert/message/$',message_info,name="message_info"),
            url(r'^mark/message/$',mark_all_message,name="mark_all_message"),
        #url(r'^role/edit/(?P<id>\d+)$',edit_role,name="edit_role"),
        #url(r'^role/remove$',remove_role,name="remove_role"),
)
