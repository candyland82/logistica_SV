# cotizaciones/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, DetalleEnvio

# Formulario para el Encabezado
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['tipo_servicio'] 
        widgets = {
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para cada Detalle de Envío (Paquete)
class DetalleEnvioForm(forms.ModelForm):
    class Meta:
        model = DetalleEnvio
        exclude = ('cotizacion',) 
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Ropa, Electrónica'}),
            'peso_lb': forms.NumberInput(attrs={'placeholder': 'Peso en libras'}),
            'largo_cm': forms.NumberInput(attrs={'placeholder': 'Largo en cm'}),
            'ancho_cm': forms.NumberInput(attrs={'placeholder': 'Ancho en cm'}),
            'alto_cm': forms.NumberInput(attrs={'placeholder': 'Alto en cm'}),
            'valor_declarado_usd': forms.NumberInput(attrs={'placeholder': 'Valor en USD'}),
        }

# Formset para manejar múltiples detalles (paquetes)
DetalleEnvioFormSet = inlineformset_factory(
    Cotizacion,           # Modelo Padre
    DetalleEnvio,         # Modelo Hijo
    form=DetalleEnvioForm,
    extra=1,              
    can_delete=True,
    fields=['descripcion', 'peso_lb', 'largo_cm', 'ancho_cm', 'alto_cm', 'valor_declarado_usd'] 
)