from django import template


register = template.Library()

@register.filter(name='multiply')
def multiply(value1, value2):
    return value1 * value2