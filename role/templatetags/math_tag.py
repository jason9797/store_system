from django import template

register = template.Library()


@register.filter
def percentage(value, total):
    try:
        return "%.2f%%" % ((float(value) / float(total)) * 100)
    except ValueError:
        return ''


@register.filter
def cut_money(value, per):
    try:
        return value*per
    except:
        return 0
