from django import template

register = template.Library()

@register.filter
def is_vendor(user):
    try:
        return hasattr(user, 'vendor')
    except:
        return False
