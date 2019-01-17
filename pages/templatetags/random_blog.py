from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

import random

register = template.Library()

@register.simple_tag
def random_bg_blog():
    num = random.randint(0,4)
    if num == 0:
        url = static('images/b_blog1.jpg')
    elif num == 1:
        url = static('images/b_blog2.jpg')
    elif num == 2:
        url = static('images/b_blog3.jpg')
    else:
        url = static('images/b_blog4.jpg')

    return url