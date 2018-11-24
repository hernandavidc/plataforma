from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Cliente, Veterinaria
from pets.models import Servicios
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from pages.models import Page

from plataforma.utils import get_rol


@method_decorator(login_required, name="dispatch")
class homeView(TemplateView):
    template_name = "profiles/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if get_rol(self.request) == 'c':
            context['cant_vete'] = Veterinaria.objects.all().count()
            context['cant_servi'] = Servicios.objects.filter(cliente=self.request.user.perfil_c.cc).count()
            context['entradas'] = Page.objects.all()[:3]
            context['rol'] = 'c'
        
        return context

@method_decorator(login_required, name="dispatch")   
class ClienteListView(ListView):
    model = Cliente
    template_name = 'profiles/profile_list.html'
    paginate_by = 8

@method_decorator(login_required, name="dispatch")
class ClienteDetailView(DetailView):

    model = Cliente
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        return get_object_or_404(Cliente, user__username=self.kwargs['username'])
