from django.db import models
from django.conf import settings

# Modelo 3: Tabla de Precios del Mercado
class PrecioMercado(models.Model):
    TIPO_SERVICIO_CHOICES = [
        ('IMP', 'Importación (EE. UU. a El Salvador)'),
        ('EXP', 'Exportación (El Salvador a EE. UU.)'),
    ]
    tipo_servicio = models.CharField(max_length=3, choices=TIPO_SERVICIO_CHOICES, unique=True)
    precio_libra = models.DecimalField(max_digits=5, decimal_places=2, help_text="Costo por libra en USD")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_tipo_servicio_display()} - ${self.precio_libra}/lb"

# Modelo 1: Cotización (Encabezado)
class Cotizacion(models.Model):
    # Relación con tu usuario personalizado
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Datos del servicio
    TIPO_SERVICIO_CHOICES = [
        ('IMP', 'Importación (EE. UU. a El Salvador)'),
        ('EXP', 'Exportación (El Salvador a EE. UU.)'),
    ]
    tipo_servicio = models.CharField(max_length=3, choices=TIPO_SERVICIO_CHOICES)
    
    # Fechas y estado
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('PEND', 'Pendiente'),
        ('PROC', 'En Proceso'),
        ('COMP', 'Completada'),
    ]
    estado = models.CharField(max_length=5, choices=ESTADO_CHOICES, default='PEND')
    
    def __str__(self):
        return f'Cotización #{self.id} de {self.usuario.username}'

    @property
    def costo_total_usd(self):
        """Calcula el costo total: Peso Total * Precio por Libra"""
        # 1. Calcular peso total
        peso_total = 0
        for detalle in self.detalles.all():
            if detalle.peso_lb:
                peso_total += detalle.peso_lb
        
        # 2. Obtener precio del mercado
        try:
            precio_mercado = PrecioMercado.objects.get(tipo_servicio=self.tipo_servicio)
            tarifa = precio_mercado.precio_libra
        except PrecioMercado.DoesNotExist:
            tarifa = 0 
            
        return peso_total * tarifa

# Modelo 2: Detalle del Paquete o Envío
class DetalleEnvio(models.Model):
    # Relaciona este detalle con la cotización padre
    cotizacion = models.ForeignKey(Cotizacion, related_name='detalles', on_delete=models.CASCADE)
    
    # Dimensiones y peso
    descripcion = models.CharField(max_length=255, help_text="Ej: Ropa, Electrónica, Documentos")
    peso_lb = models.DecimalField(max_digits=6, decimal_places=2)
    largo_cm = models.DecimalField(max_digits=6, decimal_places=2)
    ancho_cm = models.DecimalField(max_digits=6, decimal_places=2)
    alto_cm = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Valor declarado
    valor_declarado_usd = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Paquete en Cotización {self.cotizacion.id}'