# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.veiculos, name='veiculos'),
    path('cadastro/', views.veiculo_cadastro, name='veiculo_cadastro'),
    path('cadastro/auth/', views.veiculo_cadastro_auth,
        name='veiculo_cadastro_auth'),
    path('pegar-cordenadas', views.pegar_cordenadas, name='pegar_cordenadas'),
    path('pegar-cordenadas/save', views.salvar_cordenadas,
         name='salvar_cordenadas'),
    path('historico/<str:placa>/', views.historico, name='historico'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),  # noqa: E501
    path('completo/<int:id>/', views.veiculo_completo, name='veiculo_completo'),  # noqa: E501
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # noqa: E501
