# usuarios/forms.py

from django.contrib.auth.forms import UserCreationForm ,UserChangeForm #<--traigo todo de django.contrib.auth.forms

from .models import Usuario # Importa tu modelo de usuario

# Este formulario será usado para el registro de nuevos usuarios
class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Usamos tu modelo personalizado
        model = Usuario
        # Incluye los campos que quieres en el formulario de registro
        fields = ('username', 'email')

# 2. Formulario para editar el perfil (Necesario para admin.py)
# Copia y pega esta clase:
class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        # Nota: Aquí puedes listar los campos que quieres que se puedan editar.
        fields = ('username', 'email')