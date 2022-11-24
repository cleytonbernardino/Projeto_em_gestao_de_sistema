# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.veiculos, name='veiculos'),
    path('cadastro/', views.vehicle_registration, name='veiculo_cadastro'),
    path('cadastro/auth/', views.registration_vehicle_auth,
         name='veiculo_cadastro_auth'),

    path('pegar-cordenadas', views.pegar_cordenadas, name='pegar_cordenadas'),
    path('pegar-cordenadas/save', views.salvar_cordenadas,
         name='salvar_cordenadas'),

    path('historico/<str:license_plate>/', views.historic, name='historico'),
    path('pesquisa/', views.search, name='search'),  # noqa: E501
    path('completo/<str:license_plate>/', views.complete_vehicle, name='complete_vehicle'),  # noqa: E501
    path('completo/editar/<str:license_plate>/', views.edit_vehicle, name='edit'),  # noqa: E501
    path('completo/editar/auth/<str:license_plate>/',
         views.edit_vehicle_auth, name='edit_auth'),

    path("completo/apagar/<str:license_plate>", views.delete_vehicle, name="delete"),  # noqa: E501
]
