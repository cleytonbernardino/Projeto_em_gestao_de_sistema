from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users, name='users'),
    path('cadastro/', views.user_registration, name='user_registration'),
    path('cadastro/auth', views.user_registration_auth,
         name='user_registration_auth'),
    path('cadastro/detalhado/<int:id>/',
         views.detailed_user, name='detailed_user'),
    path('cadastro/detalhado/delete/<int:id>',
         views.delete_user, name='delete'),
]
