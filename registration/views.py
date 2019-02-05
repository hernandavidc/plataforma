from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms

from .forms import UserCreationFormWithEmail, UserCreationFormWithEmailVete, ClienteForm, EmailForm, VeterinariaForm
from .models import Cliente, Veterinaria
from plataforma.utils import get_rol

class SignupView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?ok'

    def get_form(self, form_class=None):
        form = super(SignupView, self).get_form()
        #Modificar campos en "tiempo rela" del formulario signup para no perder validaciones
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repite la Contraseña'})
        return form

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            perfil = Cliente(user=user)
            perfil.cc = request.POST['cc']
            perfil.save()
            return HttpResponseRedirect('/accounts/login/?ok')
        return render(request, self.template_name, {'form': form})

class SignupVeteView(CreateView):
    form_class = UserCreationFormWithEmailVete
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?ok'

    def get_form(self, form_class=None):
        form = super(SignupVeteView, self).get_form()
        #Modificar campos en "tiempo rela" del formulario signup para no perder validaciones
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repite la Contraseña'})
        return form

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):

    form_class = ClienteForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        #recuperamos el objeto que se va editar
        user_rol = get_rol(self.request)
        if user_rol == 'c':
            self.form_class = ClienteForm
            cliente = Cliente.objects.get(user=self.request.user)
            return cliente
        elif user_rol == 'v':
            self.form_class = VeterinariaForm
            vete = Veterinaria.objects.get(user=self.request.user)
            return vete
        else:
            return HttpResponse("No cuenta con perfil, pongase en contacto con servicio al cliente", status=404)
        
@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('home')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        #recuperamos el objeto que se va editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form