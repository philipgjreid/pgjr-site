# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_label(value, arg):
    return arg.get(value, value)

@register.filter
def subtract(value1, value2):
    return value1 - value2

@register.filter
def add_up(value1, value2):
    return value1 + value2

@register.filter
def divide(value1, value2):
    return value1 / value2

@register.filter
def int_null_label(value):
    if value == -1:
        return '-'
    return value

@register.filter(name='startswith')
def startswith(value, arg):
    return value.startswith(arg)
