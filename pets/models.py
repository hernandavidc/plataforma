from django.db import models
from django.contrib.auth.models import User
from registration.models import Cliente, Veterinaria

#'1era letra del nombre en español','Nombre del animal en español'
ANIMAL_CHOICE = (
     ('m','Mamífero'),
     ('p','Pez'),
     ('b','Ave'), #brid
     ('a','Anfibios'),
     ('r','Reptil'),
     ('o','Otro'),
)

def custom_upload_to(instance, filename):
    old_instance = Mascota.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'mascotas/' + filename

class Mascota(models.Model):
    dueno = models.ForeignKey(User, verbose_name="Dueño", related_name="get_pets", on_delete=models.PROTECT)
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    raza = models.CharField(verbose_name="Raza", max_length=50)
    fechaDeNacimiento = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    avatar = models.ImageField(verbose_name="Foto",upload_to=custom_upload_to, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField()
    tipo = models.CharField(max_length=1, choices= ANIMAL_CHOICE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def save(self, *args, **kwargs):
        if not self.activo:
              self.activo = True
        super(Mascota, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id) + " " + self.nombre

class AnotacionMascota(models.Model):
    creador = models.ForeignKey(User, verbose_name="Creador anotacion", on_delete=models.PROTECT)
    texto = models.CharField(verbose_name="anotacion", max_length=400)
    mascota = models.ForeignKey(Mascota, verbose_name="Mascota", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Anotacion mascota"
        verbose_name_plural = "Anotaciones mascotas"
        ordering = ['-id']

class TiposServicios(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField()

    class Meta:
        verbose_name = "Tipo de servicio"
        verbose_name_plural = "Tipos de servicios"
        ordering = ['-id']

    def __str__(self):
        return self.nombre 

class Camara(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    ip = models.CharField(verbose_name="Camara", max_length=150)
    veterinaria = models.ForeignKey(Veterinaria, related_name="get_camaras", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return self.nombre  


class Servicios(models.Model):
    fechaInicio = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
    fechaFin = models.DateField(verbose_name="Fecha final", blank=True, null=True)
    tipo = models.ForeignKey(TiposServicios, on_delete=models.PROTECT)
    camara = models.ForeignKey(Camara, on_delete=models.PROTECT, related_name='get_servicios')
    cliente = models.PositiveIntegerField(verbose_name="Cc dueño")
    mascota = models.ForeignKey(Mascota, verbose_name="Mascota", on_delete=models.PROTECT, blank=True, null=True)
    veterinaria = models.ForeignKey(Veterinaria, verbose_name="Veterinaria", on_delete=models.PROTECT)
    estado = models.BooleanField(default="True")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-created']

    def __str__(self):
        return "Rut: " + self.veterinaria.rut + " Cc: " + str(self.cliente) + " Mascota: " + self.mascota.nombre  
