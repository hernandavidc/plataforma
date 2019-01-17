from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse

from pages.models import Page
from pets.models import Servicios, Camara
from registration.models import Cliente, Veterinaria

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
        elif get_rol(self.request) == 'v':
            context['cant_cam'] = Camara.objects.filter(veterinaria=Veterinaria.objects.get(user=self.request.user)).count()
            context['cant_servi'] = Servicios.objects.filter(veterinaria=Veterinaria.objects.get(user=self.request.user)).count()
            context['entradas'] = Page.objects.all()[:3]
            context['rol'] = 'v'
        return context

@login_required
def checkClient(request, cc):
    if get_rol(request) == 'v':
        try:
            cliente = Cliente.objects.get(cc=cc)
            mascotas = cliente.user.get_pets.all()
            mascotasList = []
            for mascota in mascotas:
                if mascota.activo:
                    data = [mascota.id, mascota.nombre]
                    mascotasList.append(data)
            if cliente.user.first_name or cliente.user.last_name:
                nombre_completo = cliente.user.first_name + ' ' + cliente.user.last_name
            else:
                nombre_completo = cliente.user.username
            return JsonResponse({'nombre':nombre_completo,'mascotas':mascotasList, 'e':0})
        except Cliente.DoesNotExist:
            return JsonResponse({'nombre':"No existe perfil", 'e':1})
    else:
        return JsonResponse({'error':'No eres una veterinaria'})


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
