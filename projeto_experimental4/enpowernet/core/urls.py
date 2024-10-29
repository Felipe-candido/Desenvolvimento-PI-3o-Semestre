from django.contrib import admin
from django.urls import include, path
from . import views
from .views import add_usuario, realizar_login, logout, add_usuario2, perfil

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', add_usuario2, name='add_usuario2'),
    # path('registro/', add_usuario, name='add_usuario'),
    path('login/', realizar_login, name='realizar_login'),
    path("logout/", logout, name="logout"),
    path("perfil/", perfil, name="perfil"),
]