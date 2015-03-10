#__author__ = 'jason_lee'
from django.conf.urls import *
from views import *
urlpatterns=patterns('',
            url(r'^home$',home,name='home'),
	    url(r'^login$',mylogin,name='login'),
	    url(r'^logout$',mylogout,name='logout'),
        url(r'^role$',role_info,name='role_info'),
        url(r'^role/add/(?P<role>[0,1])$',add_role,name='add_role'),
	    #url(r'^changepassword/(?P<username>\w+)/$',changepassword,name='changepassword'),
)