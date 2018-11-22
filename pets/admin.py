from django.contrib import admin
from .models import Mascota, Servicios, TiposServicios, Camara

class ServiciosAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')
    ordering = ('created',)
    search_fields = ('veterinaria', 'cliente', 'mascota')
    list_filter = ('veterinaria', 'cliente')

    def post_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all().order_by("name")])
    post_categories.short_description = "Categorías"

class CamaraAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')
    ordering = ('created',)
    search_fields = ('nombre',)

admin.site.register(Mascota)
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(TiposServicios)
admin.site.register(Camara, CamaraAdmin)
