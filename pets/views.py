from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime

from .forms import MascotaAddOwner, ServicioAdd, CamaraAdd

from plataforma.utils import get_rol, get_perfil
from registration.models import Cliente, Veterinaria
from .models import Mascota,AnotacionMascota, Servicios, TiposServicios, Camara

@method_decorator(login_required, name="dispatch")
class MascotaUpdate(UpdateView):
    model = Mascota
    fields = ['dueno', 'nombre', 'raza', 'fechaDeNacimiento', 'tipo', 'observaciones']
    template_name_suffix = '_update_form'

    def get_object(self):
        return get_object_or_404(Mascota, id=self.kwargs['mascotaId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.filter(mascota=self.get_object())
        context['anotaciones'] = AnotacionMascota.objects.filter(mascota=self.get_object())
        context['mascotaId'] = self.kwargs['mascotaId']
        return context

def add_anotacion(request, mascotaId):
    json_responder = {'created':False}
    if request.user.is_authenticated:
        contenido = request.GET.get('content', None)
        if contenido:
            anotacion = AnotacionMascota.objects.create(creador=request.user, texto=contenido, mascota=Mascota.objects.get(id=mascotaId))
            json_responder['created'] = True
    else:
        raise Http404("El usuario no esta autenticado")
    return JsonResponse(json_responder)

@method_decorator(login_required, name="dispatch")
class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaAddOwner
    success_url = reverse_lazy('pet_list')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueno = request.user
            mascota.fechaDeNacimiento = request.POST['fechaDeNacimiento']
            mascota.save()
            return HttpResponseRedirect('/mascotas/?ok')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class ServicioCreate(CreateView):
    model = Servicios
    form_class = ServicioAdd
    success_url = reverse_lazy('servicios_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_servicios'] = TiposServicios.objects.all()
        context['camaras'] = Camara.objects.filter(veterinaria=self.request.user.perfil_v)
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            m = Mascota.objects.get(id=request.POST['mascota'])
            c = Cliente.objects.get(cc=request.POST['cliente'])
            lastSer = Servicios.objects.filter(mascota=m).first()
            print(request.POST['fechaInicio'])
            if m in c.user.get_pets.all():
                if (datetime.date(datetime.strptime(request.POST['fechaInicio'], '%Y-%m-%d')) > lastSer.fechaFin):
                    servicio.fechaInicio = request.POST['fechaInicio']
                    servicio.fechaFin = request.POST['fechaFin']
                    servicio.veterinaria = request.user.perfil_v
                    servicio.tipo = TiposServicios.objects.get(id=request.POST['tipo'])
                    servicio.camara = Camara.objects.get(id=request.POST['camara'])
                    print(request.user.id)
                    servicio.save()
                    return HttpResponseRedirect('/servicios/?ok')
                else:
                    return HttpResponseRedirect('/servicios/?noF')
            else:
                return HttpResponseRedirect('/servicios/?noM')
        else:
            return HttpResponseRedirect('/servicios/?error')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class listServices(ListView):
    template_name = "pets/list_services.html"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        r = get_rol(self.request)
        if r == 'n':
            return HttpResponseRedirect('/mascotas/')
        return super(listServices, self).get(request, *args, **kwargs)
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = get_rol(self.request)
        if r == 'v':
            context['title'] = 'Servicios'
        elif r == 'c':
            context['title'] = 'Mis servicios'
        else:
            context['title'] = 'Error: no perfil, pongase en contacto con el servicio al cliente'
        return context

    def get_queryset(self):
        r = get_rol(self.request)
        if r == 'v':
            vet = Veterinaria.objects.get(user=self.request.user)
            return Servicios.objects.filter(veterinaria=vet)
        elif r == 'c':
            client = Cliente.objects.get(user=self.request.user)
            return Servicios.objects.filter(cliente=client.cc)
        else:
            return Servicios.objects.filter(veterinaria=0)

@method_decorator(login_required, name="dispatch")
class serviceDetail(DetailView):
    model = Servicios

@method_decorator(login_required, name="dispatch")
class CamaraCreate(CreateView):
    model = Camara
    form_class = CamaraAdd
    success_url = reverse_lazy('camara_list')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            camara = form.save(commit=False)
            camara.veterinaria = request.user.perfil_v
            camara.save()
            return HttpResponseRedirect('/camaras/?ok')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name="dispatch")
class listCamara(ListView):
    template_name = "pets/list_camara.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = get_rol(self.request)
        if r == 'c':
            context['title'] = 'Error'
        elif r == 'v':
            context['title'] = 'Camaras'
        else:
            context['title'] = 'Error: no perfil, pongase en contacto con el servicio al cliente'
        return context

    def get_queryset(self):
        r = get_rol(self.request)
        if r == 'v':
            return Camara.objects.filter(veterinaria=self.request.user.perfil_v)
        else:
            return Camara.objects.filter(veterinaria=0)

@method_decorator(login_required, name="dispatch")
class listPet(ListView):
    template_name = "pets/list_pet_pre.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = get_rol(self.request)
        if r == 'c':
            context['title'] = 'Mis mascotas'
        elif r == 'v':
            context['title'] = 'Mascotas'
        else:
            context['title'] = 'Error: no perfil, pongase en contacto con el servicio al cliente'
        return context

    def get_queryset(self):
        r = get_rol(self.request)
        if r == 'c':
            return Mascota.objects.filter(dueno=self.request.user)
        else:
            return Mascota.objects.all()