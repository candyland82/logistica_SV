# usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm # Importamos tus formularios

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Formulario para crear usuarios desde el panel de admin
    add_form = UsuarioCreationForm
    # Formulario para editar usuarios existentes
    form = UsuarioChangeForm 
    # Modelo al que se aplica
    model = Usuario
    
    # Personaliza los campos visibles en la lista de usuarios
    list_display = ['username', 'email', 'is_active', 'is_staff']
    
    # Personaliza los campos de adición de usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('activation_token',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('activation_token',)}),
    )