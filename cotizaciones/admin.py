from django.contrib import admin
from .models import Cotizacion, DetalleEnvio, PrecioMercado

class DetalleEnvioInline(admin.TabularInline):
    model = DetalleEnvio
    extra = 1

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo_servicio', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'tipo_servicio')
    inlines = [DetalleEnvioInline]

@admin.register(PrecioMercado)
class PrecioMercadoAdmin(admin.ModelAdmin):
    list_display = ('tipo_servicio', 'precio_libra', 'fecha_actualizacion')
