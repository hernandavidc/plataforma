from django.contrib import admin
from .models import Mascota, Servicios, TiposServicios

class ServiciosAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')
    ordering = ('created',)
    search_fields = ('veterinaria', 'cliente', 'mascota')
    list_filter = ('veterinaria', 'cliente')

    def post_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all().order_by("name")])
    post_categories.short_description = "Categorías"

admin.site.register(Mascota)
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(TiposServicios)
