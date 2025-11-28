from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction 
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import CotizacionForm, DetalleEnvioFormSet
from .models import Cotizacion

@login_required
def crear_cotizacion(request):
    """
    Vista protegida para crear una Cotización y múltiples DetalleEnvio (paquetes)
    """
    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST)
        
        with transaction.atomic():
            if cotizacion_form.is_valid():
                cotizacion = cotizacion_form.save(commit=False)
                cotizacion.usuario = request.user
                cotizacion.save()
                
                formset = DetalleEnvioFormSet(request.POST, instance=cotizacion)
                
                if formset.is_valid():
                    formset.save()
                    messages.success(request, f'¡Cotización #{cotizacion.id} creada exitosamente!')
                    return redirect('perfil') 
                else:
                    pass
    else:
        cotizacion_form = CotizacionForm()
        formset = DetalleEnvioFormSet(instance=None)
        
    return render(request, 'cotizaciones/crear_cotizacion.html', {
        'cotizacion_form': cotizacion_form,
        'formset': formset,
    })

# --- NUEVAS VISTAS ---

class CotizacionListView(LoginRequiredMixin, ListView):
    model = Cotizacion
    template_name = 'cotizaciones/lista_cotizaciones.html'
    context_object_name = 'cotizaciones'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        # Si es staff, ve todas. Si no, solo las suyas.
        if self.request.user.is_staff:
            return Cotizacion.objects.all().order_by('-fecha_creacion')
        return Cotizacion.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

class CotizacionDetailView(LoginRequiredMixin, DetailView):
    model = Cotizacion
    template_name = 'cotizaciones/detalle_cotizacion.html'
    context_object_name = 'cotizacion'

    def get_queryset(self):
        # Asegurar que solo vea las suyas a menos que sea staff
        if self.request.user.is_staff:
            return Cotizacion.objects.all()
        return Cotizacion.objects.filter(usuario=self.request.user)

class CotizacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cotizacion
    fields = ['estado', 'tipo_servicio'] # Staff puede editar estado y tipo
    template_name = 'cotizaciones/editar_cotizacion.html'
    success_url = reverse_lazy('lista_cotizaciones')

    def test_func(self):
        # Solo staff puede editar
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar cotizaciones.")
        return redirect('perfil')