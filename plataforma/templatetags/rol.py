from django import template
from registration.models import Cliente, Veterinaria

register = template.Library()

@register.simple_tag(takes_context=True)
def rol(context):
    request = context['request']
    if Cliente.objects.filter(user=request.user).first():
        return 'c'
    elif Veterinaria.objects.filter(user=request.user).first():
        return 'v'
    else:
        return None