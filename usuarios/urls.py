# usuarios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Ruta para el registro (usando la vista de función)
    path('registro/', views.registro, name='registro'),
    
    # Ruta para el login (usando la vista genérica basada en clase)
    path('login/', views.LoginView.as_view(), name='login'),
    
    # Ruta para el logout (usando la vista genérica basada en clase)
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Ruta para la página de aterrizaje (landing page)
    path('', views.landing, name='landing'),
    
    # NUEVA RUTA: Ruta de activación de cuenta
    path('activar-cuenta/', views.activar_cuenta, name='activar_cuenta'),

    # Ruta del Dashboard (Perfil)
    path('perfil/', views.perfil, name='perfil'),
    # NUEVA RUTA: Para el enlace "Ya tengo una cuenta"
    path('forzar-login/', views.pre_login, name='pre_login'),
]
