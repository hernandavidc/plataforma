import random
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.simple_tag
def random_bg():
    num = random.randint(0,5)
    if num == 0:
        url = static('images/b-ver-mascota-online-1.png')
    elif num == 1:
        url = static('images/b-ver-mascota-online-2.png')
    elif num == 2:
        url = static('images/b-ver-mascota-online-3.png')
    elif num == 3:
        url = static('images/b-ver-mascota-online-4.png')
    else:
        url = static('images/b-ver-mascota-online-5.png')

    return url