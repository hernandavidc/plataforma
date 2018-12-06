from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#instance hace referencia al objeto que se esta guardando
def custom_upload_to(instance, filename):
    old_instance = Cliente.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

def custom_upload_to_v(instance, filename):
    old_instance = Veterinaria.objects.get(id=instance.id)
    old_instance.avatar.delete()
    return 'profiles/' + filename

#Se crean los perfiles en el formulario, funcion: def save(self):
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_c")
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    cc = models.PositiveIntegerField(unique=True,verbose_name="Cédula",null=True, blank=True, error_messages={'unique':"Esta cedula ya tiene vinculada una cuenta."})
    tel = models.CharField(verbose_name="Teléfono", max_length=15,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return str(self.cc)+" "+self.user.username

class Veterinaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_v")
    avatar = models.ImageField(upload_to=custom_upload_to_v, null=True, blank=True)
    address = models.CharField(verbose_name="Dirección", max_length=100)
    tel = models.CharField(verbose_name="Teléfono", max_length=15)
    rut = models.CharField(verbose_name="NIT", max_length=20,blank=True,null=True)
    latitud = models.CharField(max_length=20,blank=True,null=True)
    longitud = models.CharField(max_length=20,blank=True,null=True)
    nombre_representante = models.CharField(verbose_name="Nombre del representante", max_length=200)
    tel_representante = models.CharField(verbose_name="Teléfono del representante", max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Veterinaria"
        verbose_name_plural = "Veterinarias"

    def __str__(self):
        return self.user.username

#@receiver(post_save, sender=User)
#def ensure_profile_exists(sender, instance, **kwargs):
#    if kwargs.get('created', False):
#        Cliente.objects.get_or_create(user=instance)


