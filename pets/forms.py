from django import forms
from .models import Mascota, Servicios, Camara

class MascotaAddOwner(forms.ModelForm):

    class Meta:
        model = Mascota
        fields = ['nombre','raza']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'raza': forms.TextInput(attrs={'class':'form-control', 'placeholder':'raza'}),
        }
        labels = {
            'nombre':'',
            'raza':'',
        }

class CamaraAdd(forms.ModelForm):

    class Meta:
        model = Camara
        fields = ['nombre', 'descripcion', 'ip']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'descripcion'}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'ip'}),
            
        }
        labels = {

        }

class ServicioAdd(forms.ModelForm):

    class Meta:
        model = Servicios
        fields = ['cliente']
        widgets = {
            'cliente': forms.NumberInput(attrs={'id':'cc','class':'form-control mt-3', 'placeholder':'Cc cliente'}),            
        }
        labels = {

        }