from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect, JsonResponse, Http404
from datetime import datetime, date, timedelta

from .forms import MascotaAddOwner, ServicioAdd, CamaraAdd, ServicioUpdate

from plataforma.utils import get_rol, get_perfil
from registration.models import Cliente, Veterinaria
from .models import Mascota,AnotacionMascota, Servicios, TiposServicios, Camara

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

def del_anotacion(request, anotacionId):
    json_responder = {'delete':False}
    if request.user.is_authenticated:
        instance = AnotacionMascota.objects.get(id=anotacionId)
        if request.user == instance.creador:
            instance.delete()
            json_responder['delete'] = True
        else:
            raise Http404("No concuerda")
    else:
        raise Http404("El usuario no esta autenticado")
    return JsonResponse(json_responder)

def ServicioDelete(request, servicioId):
    if request.user.is_authenticated:
        instance = Servicios.objects.get(id=servicioId)
        if request.user.perfil_v == instance.veterinaria:
            instance.delete()
        else:
            raise Http404("No concuerda")
    else:
        raise Http404("El usuario no esta autenticado")
    return HttpResponseRedirect('/servicios/')

@login_required
def switchActivoMascota(request, pk):
    m = Mascota.objects.get(id=pk)
    if m in request.user.get_pets.all():
        new = not m.activo
        m.activo = new
        m.save()
    return HttpResponseRedirect('/mascotas/')

@method_decorator(login_required, name="dispatch")
class serviceEdit(UpdateView):
    model = Servicios
    template_name = 'pets/servicios_update_form.html'
    template_name_suffix = '_update_form'
    form_class = ServicioUpdate
    success_url = reverse_lazy('servicios_list')

    def get(self, request, *args, **kwargs):
        if request.user.perfil_v:
            servicio = get_object_or_404(Servicios, id=kwargs['pk'])
            if servicio in request.user.perfil_v.get_servicios.all():
                self.object = servicio
                return super(UpdateView, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse_lazy('servicios_list'))
        else:
            return HttpResponseRedirect(reverse_lazy('servicios_list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mascota = self.get_object().mascota
        context['tipos_servicios'] = TiposServicios.objects.all()
        context['camaras'] = Camara.objects.filter(veterinaria=self.request.user.perfil_v)
        if mascota:
            context['mascota'] = self.get_object().mascota.nombre
        else:
            context['mascota'] = ""
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST['fechaInicio'])
        print(request.POST['fechaFin'])
        print("*****************")
        print(form.is_valid())
        if form.is_valid():
            servicio = Servicios.objects.get(id=kwargs['pk'])
            if request.POST['fechaInicio'] != '':
                if Cliente.objects.filter(cc=request.POST['cliente']).exists(): #Si existe el cliente con esa CC
                    try:
                        m = Mascota.objects.get(id=request.POST['mascota']) #la mascota
                        encontrado = True
                    except MultiValueDictKeyError:
                        encontrado = False
                    c = Cliente.objects.get(cc=request.POST['cliente']) #el cliente
                    if m:
                        servicio.mascota = m
                    if m in c.user.get_pets.all() and encontrado: #Si la mascota pertenece a las mascotas del cliente
                        if Servicios.objects.filter(mascota=m).exists():
                            servicio.fechaInicio = request.POST['fechaInicio']
                            if request.POST['fechaFin'] != '':
                                servicio.fechaFin = request.POST['fechaFin']
                        else:
                            servicio.fechaInicio = request.POST['fechaInicio']
                            if request.POST['fechaFin'] != '':
                                servicio.fechaFin = request.POST['fechaFin']
                    else:
                        return HttpResponseRedirect('/servicios/?noM')
                else: 
                    servicio.fechaInicio = request.POST['fechaInicio']
                    if request.POST['fechaFin'] != '':
                        servicio.fechaFin = request.POST['fechaFin']
            print(request.POST['cliente'])
            servicio.cliente = request.POST['cliente']
            servicio.tipo = TiposServicios.objects.get(id=request.POST['tipo'])
            servicio.camara = Camara.objects.get(id=request.POST['camara'])
            servicio.save()
        else:
            print( (request, "Error"))
            return HttpResponseRedirect('/servicios/?error')
        return HttpResponseRedirect(reverse_lazy('servicios_list'))

@method_decorator(login_required, name="dispatch")
class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaAddOwner
    success_url = reverse_lazy('pet_list')

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueno = request.user
            mascota.fechaDeNacimiento = request.POST['fechaDeNacimiento']
            mascota.save()
            return HttpResponseRedirect('/mascotas/?ok')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class MascotaUpdate(UpdateView):
    model = Mascota
    fields = ['nombre', 'avatar', 'raza', 'fechaDeNacimiento', 'tipo', 'observaciones']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('pet_list')

    def get(self, request, *args, **kwargs):
        mascota = get_object_or_404(Mascota, id=kwargs['mascotaId'])
        if mascota in request.user.get_pets.all():
            self.object = self.get_object()
            return super(UpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/mascotas/')

    def get_object(self):
        mascota = get_object_or_404(Mascota, id=self.kwargs['mascotaId'])
        return mascota

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.filter(mascota=self.get_object())
        context['anotaciones'] = AnotacionMascota.objects.filter(mascota=self.get_object())
        context['mascotaId'] = self.kwargs['mascotaId']
        return context

@method_decorator(login_required, name="dispatch")
class mascotaDetail(DetailView):
    model = Mascota

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
        form = self.form_class(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            if request.POST['fechaInicio'] == '':
                return HttpResponseRedirect('/servicios/add/?noFI')
            if Cliente.objects.filter(cc=request.POST['cliente']).exists(): #Si existe el cliente con esa CC
                try:
                    m = Mascota.objects.get(id=request.POST['mascota']) #la mascota
                except MultiValueDictKeyError:
                    m = False
                c = Cliente.objects.get(cc=request.POST['cliente']) #el cliente
                
                if m:
                    servicio.mascota = m
                if m in c.user.get_pets.all() or not m: #Si la mascota pertenece a las mascotas del cliente
                    if Servicios.objects.filter(mascota=m).exists():
                        lastSer = Servicios.objects.filter(mascota=m).first()   #el ultimo servicio de la mascota
                        if lastSer.fechaFin:
                            fechaFin = datetime(lastSer.fechaFin.year, lastSer.fechaFin.month, lastSer.fechaFin.day, lastSer.fechaFin.hour, lastSer.fechaFin.minute)
                        else:
                            fechaFin =  lastSer.fechaInicio + timedelta(days=3)
                            fechaFin = datetime(fechaFin.year, fechaFin.month, fechaFin.day, fechaFin.hour, fechaFin.minute)
                        print(request.POST['fechaInicio'])
                        año = int(request.POST['fechaInicio'][:4])
                        mes = int(request.POST['fechaInicio'][5:7])
                        dia = int(request.POST['fechaInicio'][8:10])
                        hora = int(request.POST['fechaInicio'][11:13])
                        mins = int(request.POST['fechaInicio'][14:16])
                        if (datetime(año,mes, dia, hora, mins) > fechaFin):
                            #La fecha de inicio pedida es mayor a la de fin del ultimo servicio
                            servicio.fechaInicio = request.POST['fechaInicio']
                            if request.POST['fechaFin'] != '':
                                servicio.fechaFin = request.POST['fechaFin']
                        else:
                            return HttpResponseRedirect('/servicios/?noF')
                    else:
                        servicio.fechaInicio = request.POST['fechaInicio']
                        if request.POST['fechaFin'] != '':
                            servicio.fechaFin = request.POST['fechaFin']
                else:
                    return HttpResponseRedirect('/servicios/?noM')
            else: 
                servicio.fechaInicio = request.POST['fechaInicio']
                if request.POST['fechaFin'] != '':
                    servicio.fechaFin = request.POST['fechaFin']
            servicio.cc = request.POST['cliente']
            servicio.veterinaria = request.user.perfil_v
            servicio.tipo = TiposServicios.objects.get(id=request.POST['tipo'])
            servicio.camara = Camara.objects.get(id=request.POST['camara'])
            servicio.save()
            return HttpResponseRedirect('/servicios/?ok')
        else:
            return HttpResponseRedirect('/servicios/?error')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class listVeterinarias(ListView):
    model = Veterinaria
    template_name = "pets/list_veterinarias.html"

    def get(self, request, *args, **kwargs):
        r = get_rol(self.request)
        if r == 'n':
            return HttpResponseRedirect('/')
        elif r == 'v':
            return HttpResponseRedirect('/')
        return super(listVeterinarias, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = get_rol(self.request)
        if r == 'v':
            context['title'] = 'Veterinarias'
        elif r == 'c':
            context['title'] = 'Veterinarias'
        else:
            context['title'] = 'Error: no perfil, pongase en contacto con el servicio al cliente'
        return context

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
            return Servicios.objects.filter(cliente=self.request.user.perfil_c.cc)
        else:
            return Servicios.objects.filter(veterinaria=0)

@method_decorator(login_required, name="dispatch")
class serviceDetail(DetailView):
    model = Servicios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #La fecha altual aun esta dentro del rango? 
        if not self.object.fechaInicio:
            context['video'] = False
        elif not self.object.fechaFin:
            dias = timedelta(days=3)
            inicial_2 = self.object.fechaInicio + dias
            if datetime(inicial_2.year, inicial_2.month, inicial_2.day, inicial_2.hour, inicial_2.minute) >= datetime.now():
                context['video'] = True
            else:
                context['video'] = False
        else:
            if datetime(self.object.fechaFin.year, self.object.fechaFin.month, self.object.fechaFin.day, self.object.fechaFin.hour, self.object.fechaFin.minute) >= datetime.now():
                context['video'] = True
            else:
                context['video'] = False
        return context

@method_decorator(login_required, name="dispatch")
class detailVeterinarias(DetailView):
    model = Veterinaria

@method_decorator(login_required, name="dispatch")
class CamaraCreate(CreateView):
    model = Camara
    form_class = CamaraAdd
    success_url = reverse_lazy('camara_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            camara = form.save(commit=False)
            camara.veterinaria = request.user.perfil_v
            camara.save()
            return HttpResponseRedirect('/camaras/?ok')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class camaraDetail(DetailView):
    model = Camara

@method_decorator(login_required, name="dispatch")
class camaraUpdate(UpdateView):
    model = Camara
    fields = ['nombre', 'descripcion']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('camara_list')

    def get(self, request, *args, **kwargs):
        camara = get_object_or_404(Camara, id=kwargs['pk'])
        if camara in request.user.perfil_v.get_camaras.all():
            self.object = self.get_object()
            return super(UpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/camaras/')

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
