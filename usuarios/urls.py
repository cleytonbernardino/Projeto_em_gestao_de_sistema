from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('cadastro/', views.usuario_cadastro, name='usuario_cadastro'),
    path('cadastro/auth', views.usuario_cadastro_auth,
         name='usuarios_cadastro_auth'),
    path('cadastro/detalhado/<int:id>/',
         views.usuario_detalhado, name='usuario_detalhado'),
    path('cadastro/detalhado/delete/', views.delete_user, name='delete'),
]
