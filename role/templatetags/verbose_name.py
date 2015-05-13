#coding=utf-8
from django import template

register = template.Library()

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    try:
        name=instance._meta.get_field(field_name).verbose_name.title().decode('utf-8')
    except:
        name=instance._meta.get_field(field_name).verbose_name.title()
    if name == 'Id':
        return u'编号'
    else:
        return name

@register.simple_tag
def getattribute(instance,field):
    if field == 'sex':
        if getattr(instance,field)==True:
            return u'男'
        else:
            return u'女'
    return getattr(instance,field)
