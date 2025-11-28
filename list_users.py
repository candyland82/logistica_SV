import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica_SV.settings')
django.setup()

from usuarios.models import Usuario

print("--- Lista de Usuarios Registrados ---")
users = Usuario.objects.all()
if users.exists():
    for u in users:
        print(f"ID: {u.id} | Usuario: {u.username} | Email: {u.email} | Activo: {u.is_active}")
else:
    print("No hay usuarios registrados.")
print("-------------------------------------")
