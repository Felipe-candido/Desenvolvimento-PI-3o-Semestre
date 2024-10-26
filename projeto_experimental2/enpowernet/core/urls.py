from django.contrib import admin
from django.urls import include, path
from . import views
from .views import add_usuario, realizar_login, logout

urlpatterns = [
    path('', views.home),
    path('registro/', add_usuario, name='add_usuario'),
    path('login/', realizar_login, name='realizar_login'),
    path("logout/", logout, name="logout"),
]