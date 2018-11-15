from django.views.generic import TemplateView
from django.shortcuts import render

from pages.models import Page

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entradas'] = Page.objects.all()[:3]
        return context