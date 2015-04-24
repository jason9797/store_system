from django import template

register = template.Library()

@register.filter(name="percentage")
def percentage(value,total):
    try:
        return "%.4f%%" % ((float(value) / float(total)) * 100)
    except ValueError:
        return ''

