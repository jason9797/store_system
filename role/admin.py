from django.contrib import admin
from models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('user','role')
    list_display = ('user','role')
    search_fields = ('user',)
    ordering = ('user','role')

class Issuing_personAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Issuing_person,Issuing_personAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
