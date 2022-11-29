from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='_'),
    path('sobre/', views.about, name='about'),
]
