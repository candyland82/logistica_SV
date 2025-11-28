import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica_SV.settings')
django.setup()

from cotizaciones.models import PrecioMercado

# Precios iniciales
precios = [
    {'tipo': 'IMP', 'precio': 5.00},
    {'tipo': 'EXP', 'precio': 3.50},
]

print("--- Sembrando Precios de Mercado ---")
for p in precios:
    obj, created = PrecioMercado.objects.get_or_create(
        tipo_servicio=p['tipo'],
        defaults={'precio_libra': p['precio']}
    )
    if created:
        print(f"Creado: {obj}")
    else:
        print(f"Ya existe: {obj}")
print("------------------------------------")
