from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import UsuarioCreationForm
from .models import Usuario
from cotizaciones.models import Cotizacion

def landing(request):
    """Vista para la página de inicio (Landing Page) con Login integrado."""
    if request.user.is_authenticated:
        return redirect('perfil')
    
    form = AuthenticationForm()
    return render(request, 'usuarios/landing.html', {'form': form})

@login_required
def perfil(request):
    # Obtener cotizaciones del usuario
    mis_cotizaciones = Cotizacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Calcular estadísticas
    total_cotizaciones = mis_cotizaciones.count()
    pendientes = mis_cotizaciones.filter(estado='PEND').count()
    completadas = mis_cotizaciones.filter(estado='COMP').count()
    
    # Calcular gasto total
    gasto_total = 0
    for c in mis_cotizaciones:
        if hasattr(c, 'costo_total_usd') and c.costo_total_usd:
             gasto_total += c.costo_total_usd

    context = {
        'mis_cotizaciones': mis_cotizaciones[:5], # Solo las 5 más recientes para la tabla
        'total_cotizaciones': total_cotizaciones,
        'pendientes': pendientes,
        'completadas': completadas,
        'gasto_total': gasto_total,
    }
    return render(request, 'usuarios/perfil.html', context)

# --------------------------
# Vista de Registro
# --------------------------
def registro(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.activation_token = get_random_string(length=32)
            user.save()
            
            current_site = request.get_host()
            activation_link = f"http://{current_site}{reverse_lazy('activar_cuenta')}?token={user.activation_token}"

            send_mail(
                'Activa tu Cuenta en Logistica SV',
                f'Hola {user.username},\n\nGracias por registrarte. Por favor, haz clic en el siguiente enlace para activar tu cuenta:\n\n{activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, '¡Registro exitoso! Te hemos enviado un correo electrónico para que actives tu cuenta.')
            return redirect('login') 
    else:
        form = UsuarioCreationForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})

# --------------------------
# Vista de Activación de Cuenta
# --------------------------
def activar_cuenta(request):
    token = request.GET.get('token')
    
    if not token:
        messages.error(request, 'Enlace de activación inválido.')
        return redirect('login')
        
    try:
        user = Usuario.objects.get(activation_token=token)
    except Usuario.DoesNotExist:
        messages.error(request, 'El enlace de activación ya ha sido utilizado o es inválido.')
        return redirect('login')

    user.is_active = True
    user.activation_token = None
    user.save()

    messages.success(request, '¡Tu cuenta ha sido activada! Ya puedes iniciar sesión.')
    return redirect('login')


# Vistas de Login y Logout
class LoginView(auth_views.LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')

def pre_login(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')