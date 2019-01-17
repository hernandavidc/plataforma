from django.urls import path
from .views import switchActivoMascota, camaraUpdate, camaraDetail, del_anotacion, serviceEdit, ServicioDelete, mascotaDetail, detailVeterinarias, listVeterinarias, listPet, add_anotacion, MascotaCreate, listServices, ServicioCreate, listCamara, CamaraCreate, MascotaUpdate, serviceDetail

urlpatterns = [
    path('mascotas/', listPet.as_view(), name='pet_list'),
    path('mascotas/add/', MascotaCreate.as_view(), name='pet_add'),
    path('mascotas/<int:pk>/', mascotaDetail.as_view(), name='mascota_detail'),
    path('mascotas/<int:mascotaId>/edit/', MascotaUpdate.as_view(), name='mascota_update'),
    path('mascotas/<int:pk>/switch/', switchActivoMascota, name='mascota_s_activo'),
    path('anotacion/del/<int:anotacionId>/', del_anotacion, name='anotacion_del'),
    path('anotacion/add/<int:mascotaId>/', add_anotacion, name='anotacion_add'),
    path('servicios/', listServices.as_view(), name='servicios_list'),
    path('servicios/add/', ServicioCreate.as_view(), name='servicio_add'),
    path('servicios/<int:pk>/', serviceDetail.as_view(), name='service_detail'),
    path('servicios/<int:servicioId>/del/', ServicioDelete, name='service_del'),
    path('servicios/<int:pk>/edit/', serviceEdit.as_view(), name='service_edit'),
    path('camaras/', listCamara.as_view(), name='camara_list'),
    path('camaras/add/', CamaraCreate.as_view(), name='camara_add'),
    path('camaras/<int:pk>/', camaraDetail.as_view(), name='camara_detail'),
    path('camaras/<int:pk>/edit/', camaraUpdate.as_view(), name='camara_edit'),
    path('veterinarias/', listVeterinarias.as_view(), name='veterinarias_list'),
    path('veterinarias/<int:pk>/', detailVeterinarias.as_view(), name='veterinaria_detail'),
]