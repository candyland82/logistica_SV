import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica_SV.settings')
django.setup()

from cotizaciones.models import Cotizacion, DetalleEnvio

print("--- COTIZACIONES ---")
cots = Cotizacion.objects.all()
for c in cots:
    print(f"ID: {c.id} | Servicio: {c.tipo_servicio} | Estado: {c.estado} | Usuario: {c.usuario.username}")
    detalles = c.detalles.all()
    if details := detalles:
        print(f"  > Detalles ({detalles.count()}):")
        for d in detalles:
            print(f"    - Desc: {d.descripcion} | Peso: {d.peso_lb}lb | Valor: ${d.valor_declarado_usd}")
    else:
        print("  > Sin detalles.")
print("--------------------")
