from django import forms
from .models import Page

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'image','content', 'categories','order']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'categories': forms.Select(attrs={'class':'form-control'}),
            'order': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Orden'}),
        }
        labels = {
            'title':'',
            'order':'',
            'content':'Contenido',
        }