from django.contrib import admin
from django.urls import include, path
from . import views
from .views import  realizar_login, logout, add_usuario2, perfil, editar_usuario, buscar_projetos

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', add_usuario2, name='add_usuario2'),
    path('login/', realizar_login, name='realizar_login'),
    path("logout/", logout, name="logout"),
    path("perfil/", perfil, name="perfil"),
    path("perfil/editar/", editar_usuario, name="editar_usuario"),
    path("projetos/", buscar_projetos, name="projetos"),
    path('criar_projeto/', views.criar_projeto, name='criar_projeto'),
]