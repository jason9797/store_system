# coding=utf-8
from django import template
from django import forms
register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    try:
        name = instance._meta.get_field(field_name).verbose_name.title().decode(
            'utf-8')
    except:
        name = instance._meta.get_field(field_name).verbose_name.title()
    if name == 'Id':
        return u'编号'
    else:
        return name


@register.simple_tag
def getattribute(instance, field):
    if field == 'sex':
        if getattr(instance, field) == True:
            return u'男'
        else:
            return u'女'
    return getattr(instance, field)


@register.simple_tag
def get_widget(char, column_id):
    if char == 'int':
        return forms.TextInput(
            attrs={'required': True,
                   'step': '1',
                   'type': 'number'}).render(column_id, '')
    if char == 'char':
        return forms.TextInput(
            attrs={'required': True,
                   'type': 'text'}).render(column_id, '')
    if char == 'float':
        return forms.TextInput(
            attrs={'required': True,
                   'step': '0.01',
                   'type': 'number'}).render(column_id, '')
    if char == 'bool':
        return forms.TextInput(
            attrs={'required': True,
                   'type': 'checkbox'}).render(column_id, '')
    if char == 'text':
        return forms.Textarea(attrs={'required': True}).render(column_id, '')
    if char == 'datetime':
        return forms.TextInput(
            attrs={'required': True,
                   'class': 'datetimepicker'}).render(column_id, '')