#coding=utf-8
from django.contrib import admin
from models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class ProductAdmin(SimpleHistoryAdmin):
    list_filter = ('name','price','delivery_type','stock')
    list_display = ('name','price','delivery_type','get_stock')
    search_fields = ['name']
    ordering = ('name','price','delivery_type','stock')


class Stock_ProductAdmin(SimpleHistoryAdmin):
    list_filter = ('quantity','delivery_bill','product','stock')
    list_display = ('quantity','delivery_bill','product','stock')
    search_fields = ['quantity','delivery_bill','product','stock']
    ordering = ('quantity','delivery_bill','product','stock')

class OrderAdmin(SimpleHistoryAdmin):
    list_filter = ('delivery_no','fact_money','customer','issuing_person','product','state')
    list_display = ('delivery_no','fact_money','customer','issuing_person','product','state')
    search_fields = ['delivery_no']
    ordering = ('delivery_no','fact_money','customer','issuing_person','product','state')

class CustomerAdmin(SimpleHistoryAdmin):
    list_filter = ('name','sex','level')
    list_display = ('name','sex','level')
    search_fields = ['name']
    ordering = ('name','sex','level')

class Contact_infoAdmin(SimpleHistoryAdmin):
    list_filter = ('address','phone_number','customer')
    list_display = ('address','phone_number','customer')
    search_fields = ['address','phone_number']
    ordering = ('address','phone_number','customer')

class Order_StateAdmin(SimpleHistoryAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ['name']
    ordering = ('name',)

class Customer_LevelAdmin(SimpleHistoryAdmin):
    list_filter = ('level',)
    list_display = ('level',)
    search_fields = ['level']
    ordering = ('level',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Stock_Product,Stock_ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Contact_info,Contact_infoAdmin)
admin.site.register(Order_State,Order_StateAdmin)
admin.site.register(Customer_Level,Customer_LevelAdmin)
