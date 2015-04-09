#__author__ = 'jason_lee'
from django.conf.urls import *
from views import *
urlpatterns=patterns('',
            url(r'^home/$',home,name='home'),
            url(r'^permission/deny/$',permission_deny,name='permission_deny'),
	    url(r'^login/$',mylogin,name='login'),
	    url(r'^logout/$',mylogout,name='logout'),
        url(r'^role/info/$',role_info,name='role_info'),
        url(r'^user/info/$',user_info,name='user_info'),
        url(r'^user/add/$',user_add,name='user_add'),
        url(r'^user/edit/$',user_edit,name="user_edit"),
        url(r'^user/remove/$',user_remove,name="user_remove"),
        url(r'^rolename/add/$',role_name_add,name="role_name_add"),
        url(r'^rolename/edit/(?P<role_id>\d+)/$',role_name_edit,name="role_name_edit"),
        url(r'^rolename/remove/$',role_name_remove,name="role_name_remove"),
        #url(r'^(?P<username>\w+)/permission/edit/$',user_permission_edit,name="user_permission_edit"),
        url(r'^(?P<username>\w+)/group/edit/$',user_group_edit,name="user_group_edit"),
	    #url(r'^changepassword/(?P<username>\w+)/$',changepassword,name='changepassword'),
        url(r'^get/permissions/$',get_all_permissions,name="get_permissions"),
)