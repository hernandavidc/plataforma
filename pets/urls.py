from django.urls import path
from .views import mascotaDetail, detailVeterinarias, listVeterinarias, listPet, add_anotacion, MascotaCreate, listServices, ServicioCreate, listCamara, CamaraCreate, MascotaUpdate, serviceDetail

urlpatterns = [
    path('mascotas/', listPet.as_view(), name='pet_list'),
    path('mascotas/<int:pk>/', mascotaDetail.as_view(), name='mascota_detail'),
    path('mascotas/<int:mascotaId>/edit/', MascotaUpdate.as_view(), name='mascota_update'),
    path('anotacion/add/<int:mascotaId>/', add_anotacion, name='anotacion_add'),
    path('mascotas/add/', MascotaCreate.as_view(), name='pet_add'),
    path('servicios/', listServices.as_view(), name='servicios_list'),
    path('servicios/add/', ServicioCreate.as_view(), name='servicio_add'),
    path('servicios/<int:pk>/', serviceDetail.as_view(), name='service_detail'),
    path('camaras/', listCamara.as_view(), name='camara_list'),
    path('camaras/add/', CamaraCreate.as_view(), name='camara_add'),
    path('veterinarias/', listVeterinarias.as_view(), name='veterinarias_list'),
    path('veterinarias/<int:pk>/', detailVeterinarias.as_view(), name='veterinaria_detail'),
]