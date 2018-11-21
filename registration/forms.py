from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Cliente, Veterinaria

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido 254 caracteres como máximo y debe ser valido")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email

    def save(self):
        user = super(UserCreationFormWithEmail, self).save()
        perfil = Cliente(user=user)
        perfil.save()
        return user

class UserCreationFormWithEmailVete(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido 254 caracteres como máximo y debe ser valido")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email
        
    def save(self):
        user = super(UserCreationFormWithEmailVete, self).save()
        perfil = Veterinaria(user=user)
        perfil.save()
        return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['avatar', 'bio', 'cc', 'tel']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'cc': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Cédula de ciudadanía'}),
            'tel': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de contacto'}),
        }
        labels = {
            'avatar': '',
            'bio': '',
            'cc': '',
            'tel': '',
        }

class VeterinariaForm(forms.ModelForm):
    class Meta:
        model = Veterinaria
        fields = ['avatar', 'address', 'tel', 'rut', 'latitud','longitud']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'rut': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'RUT'}),
            'address': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Dirección'}),
            'latitud': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Latitud'}),
            'longitud': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Longitud'}),
            'tel': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de contacto'}),
        }
        labels = {
            'avatar': '',
            'rut': '',
            'address': '',
            'latitud': '',
            'longitud': '',
            'tel': '',
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido 254 caracteres como máximo y debe ser valido")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email
