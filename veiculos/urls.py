# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicles, name='vehicles'),
    path('cadastro/', views.vehicle_registration, name='vehicle_registration'),
    path('cadastro/auth/', views.registration_vehicle_auth,
         name='vehicle_registration_auth'),

    path('pegar-cordenadas', views.get_coordinates, name='get_coordinates'),
    path('pegar-cordenadas/save', views.save_coordinates,
         name='save_coordinates'),

    path('historico/<str:license_plate>/', views.historic, name='historic'),
    path('pesquisa/', views.search, name='search'),  # noqa: E501
    path('completo/<str:license_plate>/', views.complete_vehicle, name='complete_vehicle'),  # noqa: E501
    path('completo/editar/<str:license_plate>/', views.edit_vehicle, name='edit'),  # noqa: E501
    path('completo/editar/auth/<str:license_plate>/',
         views.edit_vehicle_auth, name='edit_auth'),

    path("completo/apagar/<str:license_plate>", views.delete_vehicle, name="delete"),  # noqa: E501
]
