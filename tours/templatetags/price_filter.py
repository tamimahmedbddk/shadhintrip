from django import template

register = template.Library()

@register.filter
def format_price(value):
    if value % 1 == 0:
        return "{:,.0f}".format(value)
    else:
        return "{:,.2f}".format(value)
