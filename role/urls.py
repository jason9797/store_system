#__author__ = 'jason_lee'
from django.conf.urls import *
from views import *
urlpatterns=patterns('',
            url(r'^home/$',home,name='home'),
	    url(r'^login/$',mylogin,name='login'),
	    url(r'^logout/$',mylogout,name='logout'),
        url(r'^role/$',role_info,name='role_info'),
        url(r'^role/add/(?P<role>\d+)/$',add_role,name='role_add'),
        url(r'^role/edit/(?P<id>\d+)/$',edit_role,name="role_edit"),
        url(r'^role/remove/$',remove_role,name="role_remove"),
        url(r'^rolename/add/$',role_name_add,name="role_name_add"),
        url(r'^rolename/remove/$',role_name_remove,name="role_name_remove"),
	    #url(r'^changepassword/(?P<username>\w+)/$',changepassword,name='changepassword'),
)