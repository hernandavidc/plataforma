from django import forms
from .models import Mascota, Servicios, Camara, ANIMAL_CHOICE

class MascotaAddOwner(forms.ModelForm):

    class Meta:
        model = Mascota
        fields = ['nombre','raza','tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'raza': forms.TextInput(attrs={'class':'form-control', 'placeholder':'raza'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            
        }
        labels = {
            'nombre':'Nombre',
            'raza':'Raza',
        }

class CamaraAdd(forms.ModelForm):

    class Meta:
        model = Camara
        fields = ['nombre', 'descripcion', 'ip']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'descripcion'}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección / URL'}),
            
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