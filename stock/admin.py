#coding=utf-8
from django.contrib import admin
from models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

class StockAdmin(SimpleHistoryAdmin):
    list_filter = ('name','detail','price','quantity','stock_type','stock_channel')
    list_display = ('name','detail','price','quantity','stock_type','stock_channel')
    search_fields = ['name','detail','price','quantity','stock_type','stock_channel']
    ordering = ('name','detail','price','quantity','stock_type','stock_channel')


class Stock_TypeAdmin(SimpleHistoryAdmin):
    list_filter = ('type_name',)
    list_display = ('type_name',)
    search_fields = ['type_name']
    ordering = ('type_name',)

class Stock_ChannelAdmin(SimpleHistoryAdmin):
    list_filter = ('company','person','phone_number')
    list_display = ('company','person','phone_number')
    search_fields = ['company','person','phone_number']
    ordering = ('company','person','phone_number')

class Stock_ManagementAdmin(SimpleHistoryAdmin):
    list_filter = ('stock_mode','stock','mode')
    list_display = ('stock_mode','stock','mode')
    search_fields = ['stock_mode','stock','mode']
    ordering = ('stock_mode','stock','mode')

class Stock_ModeAdmin(SimpleHistoryAdmin):
    list_filter = ('method','description')
    list_display = ('method','description')
    search_fields = ['method','description']
    ordering = ('method','description')


admin.site.register(Stock,StockAdmin)
admin.site.register(Stock_Type,Stock_TypeAdmin)
admin.site.register(Stock_Channel,Stock_ChannelAdmin)
admin.site.register(Stock_Management,Stock_ManagementAdmin)
admin.site.register(Stock_Mode,Stock_ModeAdmin)
