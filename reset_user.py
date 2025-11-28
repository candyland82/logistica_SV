import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica_SV.settings')
django.setup()

from usuarios.models import Usuario

try:
    u = Usuario.objects.get(username='lrcandray1982')
    u.is_active = True
    u.set_password('Logistica2025!')
    u.save()
    print(f"EXITO: Usuario '{u.username}' activado y contraseña restablecida.")
except Usuario.DoesNotExist:
    print("ERROR: Usuario no encontrado.")
