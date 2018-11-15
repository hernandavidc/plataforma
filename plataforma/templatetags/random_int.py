import random
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.simple_tag
def random_bg():
    num = random.randint(0,4)
    if num == 0:
        url = static('images/b1.jpg')
    elif num == 1:
        url = static('images/b2.jpg')
    elif num == 2:
        url = static('images/b3.jpg')
    else:
        url = static('images/b4.jpg')

    return url