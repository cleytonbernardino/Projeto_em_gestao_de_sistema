from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('login/auth/', views.login_auth, name='login_auth'),
    path('sobre/', views.sobre, name='sobre'),
    path('exit/', views.exit, name='exit'),
]
