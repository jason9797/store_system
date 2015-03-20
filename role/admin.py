from django.contrib import admin
from models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

class UserProfileAdmin(SimpleHistoryAdmin):
    list_filter = ('user','role')
    list_display = ('user','role')
    search_fields = ('user',)
    ordering = ('user','role')

class RoleAdmin(SimpleHistoryAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
class Issuing_personAdmin(SimpleHistoryAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Issuing_person,Issuing_personAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
